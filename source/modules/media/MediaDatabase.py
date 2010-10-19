import os
import sqlite3

class MediaFile:
    def __init__(self, filePath):
        self.filePath = filePath

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
        self.dbConnection = self._getDatabaseConnection(databaseLocation)
        self.locations = self._loadLocationsFromDatabase()
        self.mediaFiles = self._loadFilesFromDatabase()

    def _getDatabaseConnection(self, databaseLocation):
        return sqlite3.connect(databaseLocation)

    def _loadLocationsFromDatabase(self):
        result = {}

        dbCursor = self.dbConnection.cursor()
        dbCursor.execute("SELECT `id`, `absolutePath` FROM `locations`")
        for (id, absolutePath) in dbCursor:
            result[id] = absolutePath

        return result

    def _loadFilesFromDatabase(self):
        result = {}

        dbCursor = self.dbConnection.cursor()
        dbCursor.execute("SELECT `id`, `location`, `filename` FROM `files`")
        for (id, location, filename) in dbCursor:
            fileFullPath = os.path.join(self.locations[location], filename)
            result[fileFullPath] = MediaFile(filename)

        return result

    def rescan(self):
        for locationId, locationPath in self.locations.items():
            print("Scanning folder '" + locationPath + "'")
            mediaFileList = self._scanDirectory(locationPath, [])

    def _scanDirectory(self, locationPath, mediaFileList):
        if os.path.exists(locationPath):
            for file in os.listdir(locationPath):
                fileFullPath = os.path.join(locationPath, file)
                if(os.path.isdir(fileFullPath)):
                    mediaFileList.append(self._scanDirectory(fileFullPath, mediaFileList))
                else:
                    print("Found '" + fileFullPath + "'")
                    mediaFileList.append(fileFullPath)

        return mediaFileList