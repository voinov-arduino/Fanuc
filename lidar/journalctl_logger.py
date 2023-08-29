import logging
import sys

logger = None


def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(handler)
    return logger
