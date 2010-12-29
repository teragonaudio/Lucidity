import platform

class Platform:
    MACOSX = "macosx"
    WINDOWS = "windows"
    UNKNOWN = "unknown"

    @staticmethod
    def getName():
        name = platform.system()
        if name == "Darwin":
            return Platform.MACOSX
        else:
            return Platform.UNKNOWN

class Naming:
    """Names for some objects vary depending on the platform.  This class provides
    a number of static methods to get the correct name for these things.
    """
    @staticmethod
    def commandKeyName():
        name = Platform.getName()
        if name == Platform.MACOSX:
            return "command"
        else:
            return "ctrl"