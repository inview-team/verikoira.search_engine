import logging

LOG_LEVEL = "INFO"
LOG_FORMAT = '[%(asctime)s] [%(levelname)s] "%(message)s"'
DATE_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def _create_logger() -> logging.Logger:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler.setFormatter(formatter)
    # Adding to root in order to affect wsgi logs as well
    root = logging.getLogger()
    root.addHandler(handler)

    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    return logger


logger = _create_logger()
