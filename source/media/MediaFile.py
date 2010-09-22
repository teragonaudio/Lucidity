import sys
sys.path.append('types')
from MediaTypes import MediaTypeFactory

__author__ = 'nik'

class MediaFile:
    def __init__(self, filePath):
        self.filePath = filePath
        mediaTypeFactory = MediaTypeFactory()
        self.mediaType = mediaTypeFactory.getMediaType(filePath)

    def isValidType(self):
        return self.mediaType.isValid

    def getArtist(self):
        return self.mediaType.getArtist(self.filePath)