from lucidity.search import MediaFinder
from lucidity.media import MediaDatabase

if __name__ == "__main__":
    mediaDatabase = MediaDatabase("media.db")
    mediaFinder = MediaFinder(mediaDatabase)
    searchResults = mediaFinder.find("Album")
    for mediaFile in searchResults:
        print(mediaFile)