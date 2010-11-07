class MediaFinder:
    def __init__(self, mediaDatabase):
        self._mediaDatabase = mediaDatabase
        self._defaultSearchColumns = ['title', 'artist', 'albumArtist', 'album']

    def find(self, searchQuery, inColumns = None):
        if inColumns is None:
            inColumns = self._defaultSearchColumns
        searchResults = self._mediaDatabase.search(searchQuery, inColumns)
        return searchResults
