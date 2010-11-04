from lucidity.media.MediaDatabase import MediaDatabase

if __name__ == "__main__":
    mediaDb = MediaDatabase("media.db")
    mediaDb.addLocation("/Volumes/speedy/Dropbox/Tracks")
    mediaDb.rescan()