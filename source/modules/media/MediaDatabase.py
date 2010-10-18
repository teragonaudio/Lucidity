import os
import sys

class MediaFile:
    def __init__(self, location, filename):
        self.location = location
        self.filename = filename

class MediaDatabase:
    def __init__(self, databaseLocation):
        self.mediaFiles = self.loadDatabase(databaseLocation)

    def loadDatabase(self, databaseLocation):
        return {1234 : MediaFile("foo", "bar")}

class Scanner:
    def __init__(self, mediaDatabase):
        self.mediaDatabase = mediaDatabase

    def rescan(self):
        print("Scanning folder '" + folderPath + "'")
        if os.path.exists(folderPath):
            for file in os.listdir(folderPath):
                fileFullPath = os.path.join(folderPath, file)
                if(os.path.isdir(fileFullPath)):
                    self.rescan(fileFullPath)
                else:
                    mediaFile = MediaFile(fileFullPath)
                    if(mediaFile.isValidType()):
                        self.mediaFiles[fileFullPath] = mediaFile
