import logging

logger = logging.getLogger("lucidity")
logger.setLevel(logging.DEBUG)

_consoleHandler = logging.StreamHandler()
_consoleHandler.setLevel(logging.DEBUG)

_logFormat = logging.Formatter("%(message)s")
_consoleHandler.setFormatter(_logFormat)
logger.addHandler(_consoleHandler)
