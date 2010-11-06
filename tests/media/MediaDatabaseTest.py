import sys
from lucidity.media.MediaDatabase import MediaDatabase

if __name__ == "__main__":
    mediaDb = MediaDatabase("media.db")
    mediaDb.addLocation(sys.argv[1])
    mediaDb.rescan()