from lucidity.media.media import MediaDatabase
from lucidity.media.library import MediaFinder
from time import time

if __name__ == "__main__":
    mediaDatabase = MediaDatabase("media.db")

    startTime = time()
    mediaFinder = MediaFinder(mediaDatabase)
    searchResults = mediaFinder.find("and")
    stopTime = time()
    for mediaFile in searchResults:
        safeString = mediaFile.__str__()
        print(safeString.encode("ascii", "ignore"))

    print("Total files found: ", len(searchResults))
    print("Elapsed time: ", stopTime - startTime, "seconds")