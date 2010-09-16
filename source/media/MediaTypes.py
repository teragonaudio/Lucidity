import os

__author__ = 'nik'

class MediaTypeBase:
    def __init__(self):
        self.isValid = False
        self.typeName = None

class MediaTypeAac(MediaTypeBase):
    def __init__(self):
        self.typeName = "aac"
        self.isValid = True

class MediaTypeMp3(MediaTypeBase):
    def __init__(self):
        self.typeName = "mp3"
        self.isValid = True

class MediaTypeFactory:
    def __init__(self):
        self.mediaExtensions = {
            ".mp3" : MediaTypeMp3,
            ".m4a" : MediaTypeAac
        }

    def getMediaType(self, file):
        result = MediaTypeBase()
        fileParts = os.path.splitext(file)
        if fileParts[1] is not None:
            if self.mediaExtensions.has_key(fileParts[1]):
                result = self.mediaExtensions[fileParts[1]]()

        return result