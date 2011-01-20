import logging
from lucidity.system.paths import PathFinder
from lucidity.system.status import StatusProvider

class StatusHandler(logging.Handler, StatusProvider):
    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.lastMessage = ""

    def handle(self, record):
        self.lastMessage = record.getMessage()

    def getStatusString(self):
        return self.lastMessage

logger = logging.getLogger("lucidity")
logger.setLevel(logging.DEBUG)

_consoleHandler = logging.StreamHandler()
_consoleHandler.setLevel(logging.DEBUG)

_fileHandler = logging.FileHandler(PathFinder.findUserFile("log.txt"), mode='w')
_fileHandler.setLevel(logging.DEBUG)

_logFormat = logging.Formatter("%(relativeCreated)d: %(threadName)s: %(levelname)s: %(message)s")
_consoleHandler.setFormatter(_logFormat)
_fileHandler.setFormatter(_logFormat)
logger.addHandler(_consoleHandler)
logger.addHandler(_fileHandler)

statusHandler = StatusHandler()
logger.addHandler(statusHandler)
