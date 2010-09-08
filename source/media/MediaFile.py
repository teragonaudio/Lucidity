import sys
sys.path.append('types')
from MediaTypes import MediaTypeFactory

__author__ = 'nik'

class MediaFile:
    def __init__(self, mediaPath):
        self.mediaPath = mediaPath
        mediaTypeFactory = MediaTypeFactory()
        self.mediaType = mediaTypeFactory.getMediaType(mediaPath)

    def isValidType(self):
        return self.mediaType.isValid
        