import os

class PathFinder:
    @staticmethod
    def findModule(name:"str"):
        return os.path.join(os.path.dirname(__file__), name)