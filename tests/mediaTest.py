import sys
from lucidity.media import MediaDatabase

if __name__ == "__main__":
    searchArgument = "./tests/resources"
    if len(sys.argv) == 2:
        searchArgument = sys.argv[1]

    mediaDb = MediaDatabase("media.db")
    mediaDb.addLocation(searchArgument)
    mediaDb.rescan()