import os
import lucidity
from lucidity.system.platforms import Platform

class PathFinder:
    @staticmethod
    def findModule(packageName:str, moduleName:str):
        packageDir = os.path.join(os.path.dirname(lucidity.__file__), packageName)
        return os.path.join(packageDir, moduleName)

    @staticmethod
    def findResource(type:str, name:str):
        # TODO: This should probably be located somewhere else
        resourceDir = os.path.join("resources", type)
        return os.path.join(resourceDir, name)

    @staticmethod
    def findSchemaFile(name:str):
        return PathFinder.findModule("db", name)

    @staticmethod
    def findSkin(name:str):
        skinPath = PathFinder.findResource("skins", name)
        if not os.path.exists(skinPath):
            raise Exception("Skins path '" + skinPath + "' does not exist")
        return skinPath

    @staticmethod
    def findUserFile(name:"str"):
        platformName = Platform.getName()
        if platformName == Platform.MACOSX:
            libraryPath = os.path.expanduser("~/Library/Application Support/Lucidity")
            if not os.path.exists(libraryPath):
                os.mkdir(libraryPath)
            return os.path.abspath(os.path.join(libraryPath, name))
        else:
            # If we reach here, then that means we don't know what the OS is, in which
            # case we just return a path relative to the current executing directory.
            return os.path.join(".", name)