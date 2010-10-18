from lucidity.media.MediaDatabase import MediaDatabase

if __name__ == "__main__":
    mediaDb = MediaDatabase("media.db")
    for key, mediaFile in mediaDb.mediaFiles.items():
        print(key, mediaFile.location, mediaFile.filename)