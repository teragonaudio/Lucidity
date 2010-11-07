class MediaFinder:
    def __init__(self, mediaDatabase):
        self._mediaDatabase = mediaDatabase
        self._defaultSearchColumns = ['title', 'artist', 'albumArtist', 'album']
        self._defaultGroupByColumns = ['artist', 'album']
        self._defaultOrderByColumns = [('lastPlayed', 'DESC'),
                                       ('lastModified', 'DESC'),
                                       ('artist', 'ASC'),
                                       ('title', 'ASC')]

    def find(self, searchQuery, matchFromStart = False):
        return self._mediaDatabase.search(searchQuery,
                                          searchColumns = self._defaultSearchColumns,
                                          orderByColumns = self._defaultOrderByColumns,
                                          matchFromStart = matchFromStart)
