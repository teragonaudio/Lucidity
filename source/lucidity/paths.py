import os
import platform

class PathFinder:
    @staticmethod
    def findModule(name:"str"):
        return os.path.join(os.path.dirname(__file__), name)

    @staticmethod
    def findResource(name:"str"):
        # TODO: This should probably be located somewhere else
        return os.path.join("resources", name)

    @staticmethod
    def findSkin(name:"str"):
        skinPath = PathFinder.findResource("skins/" + name)
        if not os.path.exists(skinPath):
            raise Exception("Skins path '" + skinPath + "' does not exist")
        return skinPath

    @staticmethod
    def findUserFile(name:"str"):
        platformName = platform.system()
        if platformName == "Darwin":
            libraryPath = os.path.expanduser("~/Library/Application Support/Lucidity")
            if not os.path.exists(libraryPath):
                os.mkdir(libraryPath)
            return os.path.abspath(os.path.join(libraryPath, name))
        else:
            # If we reach here, then that means we don't know what the OS is, in which
            # case we just return a path relative to the current executing directory.
            return os.path.join(".", name)