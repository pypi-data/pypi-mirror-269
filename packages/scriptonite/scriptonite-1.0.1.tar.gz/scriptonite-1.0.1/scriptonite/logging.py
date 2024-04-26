from functools import singledispatchmethod
from typing import Any
import datetime
import logging
import sys


class DeltaTimeFormatter(logging.Formatter):
    """
    adds a `delta` attribute to the record, with the relative
    time since the start of logging
    """

    def format(self, record: logging.LogRecord) -> str:
        duration = datetime.datetime.fromtimestamp(
            (record.relativeCreated / 1000), datetime.UTC)
        record.delta = duration.strftime("%H:%M:%S.%f")
        return super().format(record)


class LogFilter(logging.Filter):
    """
    Filter out some log messages based on qualifier name
    """

    def __init__(self, qualname: str) -> None:
        """
        :param qualname: log message qualifier name, the `name` field of the
                         log record. Can be a `str` or a `list of str`

        """
        self._qualname = qualname

    def filter(self, record: logging.LogRecord) -> bool:
        if type(self._qualname) is list:
            return record.name not in self._qualname
        else:
            return record.name != self._qualname


class Logger(logging.Logger):
    """
    The root logger, already setup.
    This class creates an instance of the Root Logger already configured to
    write logs to `stderr` in a chosen format.

    It can autodetect if input is a tty(interactive script) and set format to
    `cli`, i.e. plain, shorter date/time or to `json` format, with full date if
    input is not a tty, for example running from a job

    """

    FORMATS = {
        'json': {
            'format':
            '{ "DateTime": "%(asctime)s", '
            '"Name": "%(name)s", "Filename": "%(filename)s:%(lineno)d", '
            '"Level": "%(levelname)s", "Message": "%(message)s"}',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'relative': {
            'formatter': DeltaTimeFormatter,
            'format': "%(delta)s "
                      "%(levelname)-8.8s "
                      "[%(name)s/%(filename)s:%(lineno)d]: %(message)s",
            'datefmt': "%H:%M:%S"
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
        },
        'short': {
            'format': "%(message)s"
        }
    }
    """
    Predefined formats:

    - `json`: JSON message with full date
    - `cli`: plain text message with short date, just time
    - `color`: like `cli` but with colored message
    - `relative`: plain text message with relative time
    - `short`: just the message
    """

    @classmethod
    def addFormat(cls, name: str,
                  format: str,
                  datefmt: str,
                  formatter: Any | None = None) -> None:
        """
        Add a new format to the Logger class

        :param name: name of the new format
        :param format: format string
        :param datefmt: date format string
        :param formatter: a custom formatter, can be empty

        for information on the format of `format` and `datefmt` strings, please
        refer to the following documents:

        - [Log record attributes](https://docs.python.org/3/library/
                                  logging.html#logrecord-attributes)
        - [Time formatting](https://docs.python.org/3/library/
                            time.html#time.strftime)
        """
        cls.FORMATS[name] = {
            'format': format,
            'datefmt': datefmt
        }

        if formatter:
            cls.FORMATS[name]['formatter'] = formatter

    def __init__(self,
                 level: str | int = logging.INFO,
                 format: str | None = None,
                 silence: str | list | None = None):
        """
        :param level: the logging level for the root logger;
        :param format: the log message format,
                       by the default it is auto-detected
        :param silence: one or more qualifier names that we want to silence.
                   This is useful to silence logs from other modules
                   that we use in our script
        """

        # If the input is a tty use `cli` message format,
        # else use `json`
        if not format:
            # are we running interactively?
            isCli = sys.stdin and sys.stdin.isatty()
            format = "cli" if isCli else "json"

        format_ = self.FORMATS[format]

        logHandler = logging.StreamHandler()
        formatter = format_.get('formatter') or logging.Formatter
        logHandler.formatter = formatter(
            fmt=format_['format'],
            datefmt=format_['datefmt'])

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
        """
        Silence one qualname or a list of qualnames

        :param qualname: one or more qualifier names to silence

        You can pass a `str` or a `list[str]`
        """
        for handler in self._rootLogger.handlers:
            handler.addFilter(LogFilter(qualname))

    @silence.register
    def _(self, qualname: list) -> None:
        """
        Silence a list of qualnames

        :param qualname: list of qualifier names to silence
        """
        for handler in self._rootLogger.handlers:
            for qual in qualname:
                handler.addFilter(LogFilter(qual))

    def __getattr__(self, attr):
        """
        Proxy method, returns methods and attributes from the real
        root logger
        """
        return getattr(self._rootLogger, attr)
