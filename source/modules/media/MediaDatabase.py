import os
import sqlite3
import time

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

    def addLocation(self, location):
        if location not in self.locations.values():
            dbCursor = self.dbConnection.cursor()
            locationAbsolutePath = os.path.abspath(location)
            dbCursor.execute("INSERT INTO `locations` (`absolutePath`) VALUES ('?')", locationAbsolutePath)
            self._rescanLocation(locationAbsolutePath)

    def rescan(self):
        for locationId, locationPath in self.locations.items():
            self._rescanLocation(locationPath)

    def _rescanLocation(self, locationPath):
        print("Scanning folder '" + locationPath + "'")
        for filePath in self._scanDirectory(locationPath, []):
            if filePath not in self.mediaFiles:
                mediaFile = MediaFile(filePath)
                self.mediaFiles[filePath] = filePath
            #                    self._addFileToDatabase(mediaFile)

    def _scanDirectory(self, locationPath, mediaFileList):
        if os.path.exists(locationPath):
            for file in os.listdir(locationPath):
                fileFullPath = os.path.join(locationPath, file)
                if(os.path.isdir(fileFullPath)):
                    mediaFileList.append(self._scanDirectory(fileFullPath, mediaFileList))
                elif MediaFile.isValid(fileFullPath):
                    print("Found file ", file.encode("ascii", "ignore"))
                    mediaFileList.append(fileFullPath)

        return mediaFileList