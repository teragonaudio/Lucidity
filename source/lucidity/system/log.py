import logging
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

_logFormat = logging.Formatter("%(relativeCreated)d: %(threadName)s: %(levelname)s: %(message)s")
_consoleHandler.setFormatter(_logFormat)
logger.addHandler(_consoleHandler)

statusHandler = StatusHandler()
logger.addHandler(statusHandler)

logger.info("Lucidity initialized. Hello there!")
