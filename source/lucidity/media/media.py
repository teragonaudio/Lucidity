import os
import time
from id3reader import id3reader
from lucidity.db.database import Sqlite3Database
from lucidity.system.log import logger
from lucidity.system.paths import PathFinder

class MediaFile:
    @staticmethod
    def isValid(file):
        result = False

        validExtensions = ['.mp3']
        fileParts = os.path.splitext(file)
        if fileParts[1] is not None:
            if fileParts[1].lower() in validExtensions:
                result = True

        return result

    def __init__(self, absolutePath):
        self._setDefaultAttributeValues()
        self.absolutePath = absolutePath
        self.exists = False

        if self.absolutePath is not None and os.path.exists(self.absolutePath):
            self.exists = True
            lastModifiedTime = os.path.getmtime(absolutePath)
            self.lastModified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(lastModifiedTime))

    def __dir__(self):
        return ["id", "absolutePath", "title", "album", "artist", "albumArtist", "year",
                "lastModified", "lastPlayed", "playCount", "timeInSeconds", "tempo",
                "startTimeInSeconds", "stopTimeInSeconds"
        ]

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
        self.id = -1

    def readMetadataFromFile(self, filePath):
        tagReader = id3reader.Reader(filePath)
        for attribute in dir(self):
            tagValue = tagReader.getValue(attribute)
            if tagValue is not None:
                setattr(self, attribute, tagValue)

    def relativePath(self, location):
        # Slice off the location's path plus an extra character for the path separator
        sliceFromIndex = len(location) + 1
        return self.absolutePath[sliceFromIndex:]


class MediaDatabase:
    def __init__(self, databaseLocation):
        self._filesColumns = {}
        schemaFileLocation = PathFinder.findSchemaFile("media.sql")
        self._database = Sqlite3Database(databaseLocation, schemaFileLocation)
        self.locations = self._loadLocationsFromDatabase()
        self.mediaFiles = self._loadFilesFromDatabase()

    def _loadLocationsFromDatabase(self):
        result = {}

        cursor = self._database.query("SELECT `id`, `absolutePath` FROM `locations`", [], False)
        for (id, absolutePath) in cursor:
            result[id] = absolutePath

        return result

    def _loadFilesFromDatabase(self):
        result = {}

        cursor = self._database.query("PRAGMA table_info(`files`)", [], False)
        columnNames = cursor.fetchall()
        self._filesColumns = self._getColumnNamesDict(columnNames)

        for row in cursor.execute("SELECT * FROM `files`"):
            locationId = self._getRowValue(row, self._filesColumns, "locationId")
            relativePath = self._getRowValue(row, self._filesColumns, "relativePath")
            location = self.locations[locationId]
            fileFullPath = os.path.join(location, relativePath)
            mediaFile = MediaFile(fileFullPath)
            self._fillMediaFileFields(mediaFile, row, self._filesColumns)
            result[mediaFile.id] = mediaFile

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
            cursor = self._database.query("INSERT INTO `locations` (`absolutePath`) VALUES (?)", [locationAbsolutePath], True)

            # Get the index of the location just added and push it to the set
            cursor.execute("SELECT `id`, `absolutePath` FROM `locations` WHERE `absolutePath` = ?",
                           [locationAbsolutePath])
            (selectedLocation) = cursor.fetchone()
            self.locations[selectedLocation[0]] = selectedLocation[1]
            self._rescanLocation(selectedLocation)

    def rescan(self):
        for location in self.locations.items():
            self._rescanLocation(location)

    def search(self, searchQuery, searchColumns = None, groupByColumns = None,
               orderByColumns = None, matchExact = False, matchFromStart = False):
        if searchColumns is None:
            # TODO: Ack, this is ugly.  Maybe we are abusing __dir__ here
            # The dir() call will work as expected but only with an instantiated
            # object.  When calling dir(MediaFile), the default known attributes
            # are returned, and the __dir__ override doesn't get hit.
            searchColumns = dir(MediaFile(None))

        matchTypeSeparator = " OR "
        if matchExact:
            matchTypeSeparator = " AND "

        whereClause = None
        for column in searchColumns:
            if whereClause is None:
                whereClause = ""
            else:
                whereClause += matchTypeSeparator
            whereClause += '`' + column + '` LIKE "'
            if not matchFromStart:
                whereClause += '%'
            whereClause += searchQuery + '%"'

        queryString = 'SELECT `id` FROM `files` WHERE ' + whereClause
        if groupByColumns is not None and isinstance(groupByColumns, list):
            groupByString = None
            for column in groupByColumns:
                if groupByString is None:
                    groupByString = ' GROUP BY '
                else:
                    groupByString += ', '
                groupByString += '`' + column + '`'
            queryString += groupByString

        if orderByColumns is not None and isinstance(orderByColumns, list):
            orderByString = None
            for (column, orderType) in orderByColumns:
                if orderByString is None:
                    orderByString = ' ORDER BY '
                else:
                    orderByString += ', '
                orderByString += '`' + column + '` ' + orderType
            queryString += orderByString

        cursor = self._database.query(queryString, [], False)
        searchResults = []
        done = False
        while not done:
            row = cursor.fetchone()
            if row is None:
                done = True
            else:
                searchResults.append(self.mediaFiles[row[0]])
        #logger.debug("Found %d results for query '%s'", len(searchResults), searchQuery)

        return searchResults

    def _rescanLocation(self, location):
        logger.info("Scanning folder '%s'", location[1])
        totalFilesFound = 0
        newFilesFound = 0
        missingFilesFound = 0
        updatedFiles = 0

        for filePath in self._scanDirectory(location[1], []):
            mediaFile = MediaFile(filePath)
            if mediaFile.exists:
                # See if the file is already in the database
                mediaFileId = None
                mediaFile.readMetadataFromFile(filePath)
                mediaFileRelativePath = mediaFile.relativePath(location[1])
                searchResultIds = self.search(mediaFileRelativePath, ['relativePath'], matchExact = True)
                
                if isinstance(searchResultIds, list):
                    for result in searchResultIds:
                        if result.absolutePath == mediaFile.absolutePath:
                            mediaFileId = result.id
                            break

                if mediaFileId not in self.mediaFiles.keys():
                    newId = self._addFileToDatabase(mediaFile, location)
                    mediaFile.id = newId
                    newFilesFound += 1
                else:
                    # The ID is specific to the database, so this newly-created
                    # object won't have one yet.  That means that this equality
                    # comparison would fail, so we copy the ID to this object.
                    mediaFile.id = mediaFileId
                    if mediaFile != self.mediaFiles[mediaFileId]:
                        self._updateFileInDatabase(mediaFile)
                        updatedFiles += 1

                self.mediaFiles[mediaFile.id] = mediaFile
                # logger.debug(mediaFile)
                totalFilesFound += 1
            else:
                if filePath in self.mediaFiles.keys():
                    del self.mediaFiles[filePath]
                    missingFilesFound += 1

        logger.info("Found %d files, %d new, %d updated, %d missing",
                    totalFilesFound, newFilesFound, updatedFiles, missingFilesFound)

    def _scanDirectory(self, locationPath, mediaFileList):
        if os.path.exists(locationPath):
            for file in os.listdir(locationPath):
                fileFullPath = os.path.join(locationPath, file)
                if os.path.isdir(fileFullPath):
                    self._scanDirectory(fileFullPath, mediaFileList)
                elif MediaFile.isValid(fileFullPath):
                    # logger.debug("Found file '%s'", file)
                    mediaFileList.append(fileFullPath)

        return mediaFileList

    def _addFileToDatabase(self, mediaFile, location):
        otherFields = {
            'relativePath': mediaFile.relativePath(location[1]),
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
        cursor = self._database.query(queryString, queryValues, True)
        newId = cursor.lastrowid
        return newId

    def _deleteFileFromDatabase(self, mediaFile):
        self._database.query("DELETE FROM `files` WHERE `id` = ?", [mediaFile.id], True)

    def _updateFileInDatabase(self, mediaFile):
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
        self._database.query(queryString, updateValues, True)

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
