import logging

logger = logging.getLogger("lucidity")
logger.setLevel(logging.DEBUG)

_consoleHandler = logging.StreamHandler()
_consoleHandler.setLevel(logging.DEBUG)

_logFormat = logging.Formatter("%(relativeCreated)d: %(levelname)s - %(message)s")
_consoleHandler.setFormatter(_logFormat)
logger.addHandler(_consoleHandler)

logger.info("Lucidity initialized. Hello there!")
