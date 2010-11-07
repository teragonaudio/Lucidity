import os
import sqlite3
import time

from id3reader import id3reader
from lucidity.log import logger

class MediaFile:
    @staticmethod
    def isValid(file):
        result = False

        validExtensions = ['.mp3']
        fileParts = os.path.splitext(file)
        if(fileParts[1] is not None):
            if fileParts[1].lower() in validExtensions:
                result = True

        return result

    def __init__(self, absolutePath):
        self._setDefaultAttributeValues()
        self.absolutePath = absolutePath
        self.exists = os.path.exists(self.absolutePath)
        if self.exists:
            lastModifiedTime = os.path.getmtime(absolutePath)
            self.lastModifiedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(lastModifiedTime))

    def __dir__(self):
        return ["id", "absolutePath", "title", "album", "artist", "albumArtist", "year"]

    def __str__(self):
        result = None
        for attribute in dir(self):
            attr = getattr(self, attribute)
            if result == None:
                result = ""
            else:
                result += ", "
            result += attribute + ": '" + attr.__str__() + "'"
        return result

    def __eq__(self, other):
        for attribute in dir(self):
            selfAttr = getattr(self, attribute)
            otherAttr = getattr(other, attribute)
            if selfAttr != otherAttr:
                return False
        return True

    def _setDefaultAttributeValues(self):
        for attribute in dir(self):
            setattr(self, attribute, "")

    def readMetadataFromFile(self, filePath):
        tagReader = id3reader.Reader(filePath)
        for attribute in dir(self):
            tagValue = tagReader.getValue(attribute)
            if tagValue is not None:
                setattr(self, attribute, tagValue)

class MediaDatabase:
    def __init__(self, databaseLocation):
        self._databaseLocation = databaseLocation
        self._dbConnection = self._getDatabaseConnection(databaseLocation)
        self.locations = self._loadLocationsFromDatabase()
        self.mediaFiles = self._loadFilesFromDatabase()

    def _getDatabaseConnection(self, databaseLocation):
        if os.path.exists(databaseLocation):
            # TODO: Need to check database integrity
            return sqlite3.connect(databaseLocation)
        else:
            return self._createDatabase(databaseLocation)

    def _createDatabase(self, databaseLocation):
        dbConnection = sqlite3.connect(databaseLocation)
        schemaFileLocation = os.path.join(os.path.dirname(__file__), "media.sql")
        schemaFile = open(schemaFileLocation, 'r')
        dbConnection.executescript(schemaFile.read())
        schemaFile.close()
        return dbConnection

    def _loadLocationsFromDatabase(self):
        result = {}

        dbCursor = self._dbConnection.cursor()
        dbCursor.execute("SELECT `id`, `absolutePath` FROM `locations`")
        for (id, absolutePath) in dbCursor:
            result[id] = absolutePath

        return result

    def _loadFilesFromDatabase(self):
        result = {}
        dbCursor = self._dbConnection.cursor()
        dbCursor.execute("PRAGMA table_info(`files`)")
        columnNamesRow = dbCursor.fetchall()
        columnNameIndexes = self._getColumnNamesDict(columnNamesRow)

        for row in dbCursor.execute("SELECT * FROM `files`"):
            locationId = self._getRowValue(row, columnNameIndexes, "locationId")
            relativePath = self._getRowValue(row, columnNameIndexes, "relativePath")
            location = self.locations[locationId]
            fileFullPath = location + relativePath
            mediaFile = MediaFile(fileFullPath)
            self._fillMediaFileFields(mediaFile, row, columnNameIndexes)
            result[fileFullPath] = mediaFile

        return result

    def _getColumnNamesDict(self, columnNamesRow):
        result = {}
        for column in columnNamesRow:
            columnName = column[1]
            columnIndex = column[0]
            result[columnName] = columnIndex
        return result

    def _getRowValue(self, row, columnNameIndexes, columnName):
        return row[columnNameIndexes[columnName]]

    def _fillMediaFileFields(self, mediaFile, row, columnNameIndexes):
        for attribute in dir(mediaFile):
            if attribute in columnNameIndexes:
                rowValue = self._getRowValue(row, columnNameIndexes, attribute)
                setattr(mediaFile, attribute, rowValue)

    def addLocation(self, location):
        # Make sure that the location is not a subfolder any previous location
        locationFoundAsSubfolder = False
        for locationIndex, locationPath in self.locations.items():
            if locationPath.find(location) is not -1:
                locationFoundAsSubfolder = True
                break

        # TODO: Extra checks for disallowing root, non-directories, etc.
        if not locationFoundAsSubfolder:
            dbCursor = self._dbConnection.cursor()
            locationAbsolutePath = os.path.abspath(location)
            dbCursor.execute("INSERT INTO `locations` (`absolutePath`) VALUES (?)", [locationAbsolutePath])
            self._commitDatabase()

            # Get the index of the location just added and push it to the set
            dbCursor.execute("SELECT `id`, `absolutePath` FROM `locations` WHERE `absolutePath` = ?", [locationAbsolutePath])
            (selectedLocation) = dbCursor.fetchone()
            self.locations[selectedLocation[0]] = selectedLocation[1]
            self._rescanLocation(selectedLocation)

    def rescan(self):
        for location in self.locations.items():
            self._rescanLocation(location)

    def _rescanLocation(self, location):
        logger.debug("Scanning folder '%s'", location[1])
        totalFilesFound = 0
        newFilesFound = 0
        missingFilesFound = 0
        updatedFiles = 0

        for filePath in self._scanDirectory(location[1], []):
            mediaFile = MediaFile(filePath)
            if mediaFile.exists:
                mediaFile.readMetadataFromFile(filePath)

                if filePath not in self.mediaFiles.keys():
                    self._addFileToDatabase(mediaFile, location)
                    newFilesFound += 1
                else:
                    mediaFileDbCache = self.mediaFiles[filePath]
                    # The ID is specific to the database, so this newly-created
                    # object won't have one yet.  That means that this equality
                    # comparison would fail, so we copy the ID to this object.
                    mediaFile.id = mediaFileDbCache.id
                    if mediaFile != mediaFileDbCache:
                        self._updateFileInDatabase(mediaFile, location)
                        updatedFiles += 1

                self.mediaFiles[filePath] = mediaFile
                totalFilesFound += 1
            else:
                if filePath in self.mediaFiles.keys():
                    del self.mediaFiles[filePath]
                    missingFilesFound += 1

        logger.debug("Found %d files, %d new, %d updated, %d missing",
                     totalFilesFound, newFilesFound, updatedFiles, missingFilesFound)

    def _commitDatabase(self):
        self._dbConnection.commit()

    def _scanDirectory(self, locationPath, mediaFileList):
        if os.path.exists(locationPath):
            for file in os.listdir(locationPath):
                fileFullPath = os.path.join(locationPath, file)
                if(os.path.isdir(fileFullPath)):
                    self._scanDirectory(fileFullPath, mediaFileList)
                elif MediaFile.isValid(fileFullPath):
                    logger.debug("Found file '%s'", (file))
                    mediaFileList.append(fileFullPath)

        return mediaFileList

    def _addFileToDatabase(self, mediaFile, location):
        sliceIndex = len(location[1])
        mediaFileRelativePath = mediaFile.absolutePath[sliceIndex:]

        dbCursor = self._dbConnection.cursor()
        dbCursor.execute('''INSERT INTO `files`
            (`locationId`, `relativePath`, `lastModified`, `title`, `album`)
            VALUES (?, ?, ?, ?, ?)
            ''',
                         [location[0], mediaFileRelativePath, mediaFile.lastModifiedDate,
                         mediaFile.title, mediaFile.album])
        self._commitDatabase()

    def _deleteFileFromDatabase(self, mediaFile):
        dbCursor = self._dbConnection.cursor()
        dbCursor.execute("DELETE FROM `files` WHERE `id` = ?", [mediaFile.id])

    def _updateFileInDatabase(self, mediaFile, location):
        dbCursor = self._dbConnection.cursor()
        dbCursor.execute('''UPDATE `files`
            SET `title` = ?, `album` = ?
            WHERE `id` = ?''', [mediaFile.title, mediaFile.album, mediaFile.id])
        self._commitDatabase()
        pass
