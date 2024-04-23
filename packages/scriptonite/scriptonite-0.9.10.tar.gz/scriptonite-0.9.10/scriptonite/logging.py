from functools import singledispatchmethod
import logging
import sys


class LogFilter(logging.Filter):

    def __init__(self, qualname: str | list) -> None:
        self.qualname = qualname

    def filter(self, record: logging.LogRecord) -> bool:
        return not record.name == self.qualname


class Logger(logging.Logger):

    FORMATS = {
        'json': {
            'format':
            '{ "DateTime": "%(asctime)s", '
            '"Name": "%(name)s", "Filename": "%(filename)s:%(lineno)d", '
            '"Level": "%(levelname)s", "Message": "%(message)s"}',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'cli': {
            'format': "%(asctime)s "
                      "%(levelname)-8.8s "
                      "[%(name)s/%(filename)s:%(lineno)d]: %(message)s",
            'datefmt': "%H:%M:%S"
        },
        'color': {
            'format': "\x1b[0;1m%(asctime)s,%(msecs)03d "
                      "\x1b[1;31m%(levelname)-8.8s "
                      "\x1b[1;34m[%(name)s/%(filename)s:%(lineno)d]: "
                      "\x1b[0m%(message)s",
            'datefmt': "%H:%M:%S"
        }
    }

    def __init__(self,
                 level: str | int = logging.INFO,
                 format: str | None = None,
                 silence: str | list | None = None):

        # If the input is a tty use `cli` message format,
        # else use `json`
        if not format:
            # are we running interactively?
            isCli = sys.stdin and sys.stdin.isatty()
            format = "cli" if isCli else "json"

        logHandler = logging.StreamHandler()
        logHandler.formatter = logging.Formatter(
            fmt=self.FORMATS[format]['format'],
            datefmt=self.FORMATS[format]['datefmt'])

        logHandler.formatter.default_msec_format = '%s.%03d'

        # Get root logger
        rootLogger = logging.getLogger()
        # Add our handler
        rootLogger.handlers = [logHandler]
        # Set log level
        rootLogger.setLevel(level)

        # Attach it to internal reference
        self._rootLogger = rootLogger

        if silence:
            self.silence(silence)

    @singledispatchmethod
    def silence(self, qualname: str) -> None:
        for handler in self._rootLogger.handlers:
            handler.addFilter(LogFilter(qualname))

    @silence.register
    def _(self, qualname: list) -> None:
        for handler in self._rootLogger.handlers:
            for qual in qualname:
                handler.addFilter(LogFilter(qual))

    def __getattr__(self, attr):
        return getattr(self._rootLogger, attr)
