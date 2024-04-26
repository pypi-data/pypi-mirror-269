import os
import logging
from logging import StreamHandler, NullHandler, Formatter
from logging.handlers import WatchedFileHandler

_PHOUND_LOGGER_NAME = "phound"

logger = logging.getLogger(_PHOUND_LOGGER_NAME)
logger.addHandler(NullHandler())
logger.propagate = False


def setup_logging():
    is_logging_enabled, log_file_dir = get_logging_parameters()
    if not is_logging_enabled:
        return

    handler = StreamHandler()
    handler.setFormatter(_get_formatter())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info(f"Added a stderr logging handler to logger: {_PHOUND_LOGGER_NAME}")

    # WatchedFileHandler is only intended for use under Unix/Linux
    if log_file_dir and os.name == 'posix':
        _setup_file_handler(f"{log_file_dir}/phound-all.log", logging.DEBUG)
        _setup_file_handler(f"{log_file_dir}/phound-error.log", logging.ERROR)
        logger.info(f"Added a file logging handlers to logger: {_PHOUND_LOGGER_NAME}")


def get_logging_parameters():
    return (os.environ.get("PHOUND_LOG", "False").lower() == "true",
            _to_absolute_path(os.environ.get("PHOUND_LOG_DIR")))


def _setup_file_handler(path, level):
    handler = WatchedFileHandler(path)
    handler.setFormatter(_get_formatter())
    handler.setLevel(level)
    logger.addHandler(handler)


def _get_formatter():
    return Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] "
                     "[thread:%(threadName)s] [%(filename)s:%(lineno)d] %(message)s")


def _to_absolute_path(log_file_dir):
    return os.path.abspath(log_file_dir) if log_file_dir else ""
