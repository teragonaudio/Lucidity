import queue
from threading import Thread
from lucidity.core.arrangement import Item
from lucidity.core.timing import MusicTimeConverter
from lucidity.media.media import MediaDatabase, MediaFile
from lucidity.system.log import logger

#noinspection PyUnusedLocal
class MediaRequestDelegate:
    def onRequestComplete(self, request:"MediaRequest", args): pass

class MediaRequest:
    RESCAN = "rescan"
    SEARCH = "search"
    QUIT = "quit"

    def __init__(self, type:str=None, delegate:MediaRequestDelegate=None, query:str=None):
        self.type = type
        self.delegate = delegate
        self.query = query

class MediaRequestLoop(Thread):
    MAX_REQUESTS = 32

    def __init__(self, absolutePath:str):
        Thread.__init__(self, name = "MediaRequestLoop")
        self.queue = queue.Queue(self.MAX_REQUESTS)
        self._absolutePath = absolutePath
        self._mediaDatabase = None
        self.searchColumns = ['title', 'artist', 'albumArtist', 'album']
        self.groupByColumns = ['artist', 'album']
        self.orderByColumns = [('lastPlayed', 'DESC'),
                                       ('lastModified', 'DESC'),
                                       ('artist', 'ASC'),
                                       ('title', 'ASC')]
        self._isRunning = False

    def run(self):
        # The database needs to be created here because sqlite requires that
        # all requests to a database be made by the same thread.
        self._mediaDatabase = MediaDatabase(self._absolutePath)
        self._rescanLibrary()
        self._isRunning = True
        while self._isRunning:
            request = self.queue.get(block = True)
            self._processRequest(request)

    def addRequest(self, request:MediaRequest):
        try:
            self.queue.put(request, block = False)
        except queue.Full:
            logger.warn("Failed adding request, queue is full")

    def quit(self):
        self.addRequest(MediaRequest(type=MediaRequest.QUIT))

    def _processRequest(self, request:MediaRequest):
        if request.type == MediaRequest.SEARCH:
            results = self._search(request.query)
            if request.delegate is not None:
                request.delegate.onRequestComplete(request, results)
        elif request.type == MediaRequest.RESCAN:
            self._rescanLibrary()
            if request.delegate is not None:
                request.delegate.onRequestComplete(request, "Rescan finished")
        elif request.type == MediaRequest.QUIT:
            self._isRunning = False
        else:
            logger.info("Unknown media request type '" + request.type + "'")

    def _search(self, searchQuery, matchFromStart = True):
        return self._mediaDatabase.search(searchQuery,
                                          searchColumns = self.searchColumns,
                                          orderByColumns = self.orderByColumns,
                                          matchFromStart = matchFromStart)

    def _rescanLibrary(self):
        self._mediaDatabase.rescan()

class MediaFileConverter:
    @staticmethod
    def getItemForMediaFile(mediaFile:MediaFile, track:int,
                            startingPositionInBeats:int, tempo:float):
        lengthInBeats = MusicTimeConverter.secondsToBeats(tempo, mediaFile.getLength())
        return Item(mediaFile.id, track, mediaFile.getLabel(),
                    startingPositionInBeats, lengthInBeats, 0)