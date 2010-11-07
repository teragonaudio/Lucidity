from lucidity.search import MediaFinder
from lucidity.media import MediaDatabase

if __name__ == "__main__":
    mediaDatabase = MediaDatabase("media.db")
    mediaFinder = MediaFinder(mediaDatabase)
    searchResults = mediaFinder.find("syntax")
    for mediaFile in searchResults:
        safeString = mediaFile.__str__()
        print(safeString.encode("ascii", "ignore"))