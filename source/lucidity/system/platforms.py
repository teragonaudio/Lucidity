import platform

class Naming:
    """Names for some objects vary depending on the platform.  This class provides
    a number of static methods to get the correct name for these things.
    """

class Platform:
    MACOSX = ""
    WINDOWS = "windows"
    @staticmethod
    def getName():
        name = platform.system()