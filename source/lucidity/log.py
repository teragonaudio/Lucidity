import logging

logger = logging.getLogger("lucidity")
logger.setLevel(logging.INFO)

_consoleHandler = logging.StreamHandler()
_consoleHandler.setLevel(logging.INFO)

_logFormat = logging.Formatter("%(message)s")
_consoleHandler.setFormatter(_logFormat)
logger.addHandler(_consoleHandler)
