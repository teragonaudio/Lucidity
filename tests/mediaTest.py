import sys
from lucidity.media.media import MediaDatabase
from time import time

if __name__ == "__main__":
    searchArgument = "./tests/resources"
    if len(sys.argv) == 2:
        searchArgument = sys.argv[1]

    startTime = time()
    mediaDb = MediaDatabase("media.db")
    mediaDb.addLocation(searchArgument)
    # mediaDb.rescan()
    stopTime = time()
    print("Elapsed time: ", stopTime - startTime, "seconds")