from lucidity.media.MediaDatabase import MediaDatabase

if __name__ == "__main__":
    print("Rescanning locations")
    mediaDb = MediaDatabase("media.db")
    mediaDb.rescan()