# Reference:
# https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/

import logging


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[38;5;33m"
    light_blue = "\x1b[38;5;45m"
    reset = "\x1b[0m"

    def __init__(self, fmt, with_color: bool = False):
        super().__init__()
        self.fmt = fmt
        base_fmt = self.fmt + self.reset

        if with_color:
            self.FORMATS = {
                logging.DEBUG: self.grey + base_fmt,
                logging.INFO: self.light_blue + base_fmt,
                logging.WARNING: self.yellow + base_fmt,
                logging.ERROR: self.red + base_fmt,
                logging.CRITICAL: self.bold_red + base_fmt,
            }
        else:
            self.FORMATS = {level: base_fmt for level in logging._levelToName.values()}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


_LOGGER_NAME = "logger"

_FORMAT = "%(message)s"

logger = logging.getLogger(_LOGGER_NAME)
logger.setLevel(logging.DEBUG)

_formatter = CustomFormatter(_FORMAT)

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)

logger.addHandler(_stream_handler)
