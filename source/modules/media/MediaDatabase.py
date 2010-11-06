import os
import sqlite3
import time

from lucidity.logging.Logger import logger

class MediaFile:
    def __init__(self, absolutePath):
        self.absolutePath = absolutePath
        self.exists = os.path.exists(self.absolutePath)
        if self.exists:
            lastModifiedTime = os.path.getmtime(absolutePath)
            self.lastModifiedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(lastModifiedTime))

    @staticmethod
    def isValid(file):
        result = False

        validExtensions = ['.mp3', '.m4a']
        fileParts = os.path.splitext(file)
        if(fileParts[1] is not None):
            if fileParts[1].lower() in validExtensions:
                result = True

        return result

class MediaDatabase:
    def __init__(self, databaseLocation):
        self._databaseLocation = databaseLocation
        self._dbConnection = self._getDatabaseConnection(databaseLocation)
        self.locations = self._loadLocationsFromDatabase()
        self.mediaFiles = self._loadFilesFromDatabase()

    def _getDatabaseConnection(self, databaseLocation):
        if not os.path.exists(databaseLocation):
            return self._createDatabase(databaseLocation)
        else:
            # TODO: Need to check database integrity
            return sqlite3.connect(databaseLocation)

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
            result[fileFullPath] = MediaFile(fileFullPath)

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
                setattr(mediaFile, attribute, columnNameIndexes[attribute])

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

        for filePath in self._scanDirectory(location[1], []):
            mediaFile = MediaFile(filePath)
            if mediaFile.exists:
                self._addFileToDatabase(mediaFile, location)
                if filePath not in self.mediaFiles.keys():
                    newFilesFound += 1

                self.mediaFiles[filePath] = mediaFile
                totalFilesFound += 1
            else:
                if filePath in self.mediaFiles.keys():
                    del self.mediaFiles[filePath]
                    missingFilesFound += 1

        logger.debug("Found %d files, %d new, %d missing",
                     totalFilesFound, newFilesFound, missingFilesFound)

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
            (`locationId`, `relativePath`, `lastModified`)
            VALUES (?, ?, ?)
            ''',
                         [location[0], mediaFileRelativePath, mediaFile.lastModifiedDate])
        self._commitDatabase()
