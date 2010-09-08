import os
import sys

from MediaFile import MediaFile

__author__ = 'nik'

class MediaFolder:
    def __init__(self, folderPath):
        self.folderPath = folderPath
        self.mediaFiles = {}
        self.rescan(self.folderPath)

        for mediaFileKey in self.mediaFiles.keys():
            mediaFile = self.mediaFiles[mediaFileKey]
            print "GOT", mediaFileKey, ":", mediaFile.mediaType.typeName

    def rescan(self, folderPath):
        print "Scanning folder '" + folderPath + "'"
        if os.path.exists(folderPath):
            for file in os.listdir(folderPath):
                fileFullPath = os.path.join(folderPath, file)
                if(os.path.isdir(fileFullPath)):
                    self.rescan(fileFullPath)
                else:
                    mediaFile = MediaFile(fileFullPath)
                    if(mediaFile.isValidType()):
                        self.mediaFiles[fileFullPath] = mediaFile

if __name__ == "__main__":
    mediaFolder = MediaFolder(sys.argv[1])