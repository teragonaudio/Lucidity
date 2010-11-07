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
            self.lastModified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(lastModifiedTime))

    def __dir__(self):
        return ["id", "absolutePath", "title", "album", "artist", "albumArtist", "year",
                "lastModified"]

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
            selfAttr = str(getattr(self, attribute))
            otherAttr = str(getattr(other, attribute))
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
        self._filesColumns = {}
        self._databaseLocation = databaseLocation
        self._dbConnection = self._getDatabaseConnection(databaseLocation)
        self.locations = self._loadLocationsFromDatabase()
        self.mediaFiles = self._loadFilesFromDatabase()

    def _getDatabaseConnection(self, databaseLocation):
        if os.path.exists(databaseLocation):
            # TODO: Need to check database integrity, schema, etc.
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
        columnNames = dbCursor.fetchall()
        self._filesColumns = self._getColumnNamesDict(columnNames)

        for row in dbCursor.execute("SELECT * FROM `files`"):
            locationId = self._getRowValue(row, self._filesColumns, "locationId")
            relativePath = self._getRowValue(row, self._filesColumns, "relativePath")
            location = self.locations[locationId]
            fileFullPath = os.path.join(location, relativePath)
            mediaFile = MediaFile(fileFullPath)
            self._fillMediaFileFields(mediaFile, row, self._filesColumns)
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
        addLocation = True
        locationAbsolutePath = os.path.abspath(location)

        if locationAbsolutePath == os.sep:
            raise Exception("The top-level directory is not permitted for locations")
        if not os.path.exists(locationAbsolutePath):
            raise Exception("This folder does not exist")
        else:
            if not os.path.isdir(locationAbsolutePath):
                raise Exception("This location is not a directory")

        # Make sure that the location is not a subfolder any previous location
        for locationIndex, locationPath in self.locations.items():
            # Check if the location is the same as a known location, or a subfolder
            # of an already known location
            if locationAbsolutePath.find(locationPath) is not -1:
                addLocation = False
            # Jump out of this loop if the location was found
            if not addLocation: break

        if addLocation:
            dbCursor = self._dbConnection.cursor()
            dbCursor.execute("INSERT INTO `locations` (`absolutePath`) VALUES (?)", [locationAbsolutePath])
            self._commitDatabase()

            # Get the index of the location just added and push it to the set
            dbCursor.execute("SELECT `id`, `absolutePath` FROM `locations` WHERE `absolutePath` = ?",
                             [locationAbsolutePath])
            (selectedLocation) = dbCursor.fetchone()
            self.locations[selectedLocation[0]] = selectedLocation[1]
            self._rescanLocation(selectedLocation)

    def rescan(self):
        for location in self.locations.items():
            self._rescanLocation(location)

    def _rescanLocation(self, location):
        logger.info("Scanning folder '%s'", location[1])
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
                        self._updateFileInDatabase(mediaFile)
                        updatedFiles += 1

                self.mediaFiles[filePath] = mediaFile
                logger.debug(mediaFile)
                totalFilesFound += 1
            else:
                if filePath in self.mediaFiles.keys():
                    del self.mediaFiles[filePath]
                    missingFilesFound += 1

        logger.info("Found %d files, %d new, %d updated, %d missing",
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
        # Slice off the location's path plus an extra character for the path separator
        sliceFromIndex = len(location[1]) + 1
        mediaFileRelativePath = mediaFile.absolutePath[sliceFromIndex:]
        otherFields = {
            'relativePath': mediaFileRelativePath,
            'locationId': location[0]
        }
        queryFields = self._getQueryFields(mediaFile, otherFields)

        # Place fields into comma-separated strings in order to build the insert query
        queryColumns = None
        queryValuePlaceholders = None
        queryValues = []
        for (field, value) in queryFields.items():
            if queryColumns is None:
                queryColumns = ''
                queryValuePlaceholders = ''
            else:
                queryColumns += ', '
                queryValuePlaceholders += ', '

            queryColumns += '`' + field + '`'
            queryValuePlaceholders += '?'
            queryValues.append(value)

        queryString = 'INSERT INTO `files` (' + queryColumns + ') VALUES (' + queryValuePlaceholders + ')'
        dbCursor = self._dbConnection.cursor()
        dbCursor.execute(queryString, queryValues)
        self._commitDatabase()

    def _deleteFileFromDatabase(self, mediaFile):
        dbCursor = self._dbConnection.cursor()
        dbCursor.execute("DELETE FROM `files` WHERE `id` = ?", [mediaFile.id])

    def _updateFileInDatabase(self, mediaFile):
        dbCursor = self._dbConnection.cursor()
        queryFields = self._getQueryFields(mediaFile, {})

        updatePairs = None
        updateValues = []
        for (field, value) in queryFields.items():
            if updatePairs is None:
                updatePairs = ''
            else:
                updatePairs += ', '

            updatePairs += '`' + field + '` = ?'
            updateValues.append(value)

        queryString = 'UPDATE `files` SET ' + updatePairs + ' WHERE `id` = ?'
        updateValues.append(mediaFile.id)
        dbCursor.execute(queryString, updateValues)
        self._commitDatabase()
        pass

    def _getQueryFields(self, mediaFile, otherFields):
        queryFields = otherFields

        # Manually insert some fields which do not exist in the MediaFile class
        # before building a query
        for attribute in dir(mediaFile):
            if attribute in self._filesColumns:
                attributeValue = getattr(mediaFile, attribute)
                if attributeValue is not None:
                    queryFields[attribute] = attributeValue

        # This field may not be included in the query, as it is auto-incremented
        del(queryFields['id'])
        return queryFields
