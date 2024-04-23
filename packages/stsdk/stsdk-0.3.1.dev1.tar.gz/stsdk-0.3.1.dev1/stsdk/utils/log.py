import inspect
import os
import sys

from loguru import logger


class LogUtil:
    def __init__(self, log_directory = None):
        if log_directory:
            self.set_dir(log_directory)
        else:
            self.set_dir("./logs")

    def set_dir(self, log_directory):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)

        log_file_info = os.path.join(self.log_directory, "{time:YYYY-MM-DD}_info.log")
        log_file_error = os.path.join(self.log_directory, "{time:YYYY-MM-DD}_error.log")
        log_file_warning = os.path.join(
            self.log_directory, "{time:YYYY-MM-DD}_warning.log"
        )
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green> | <level>{level: <8}</level> | <cyan>{"
            "message}</cyan> "
        )
        logger.remove()
        logger.add(sys.stdout, format=log_format, colorize=True)
        logger.add(
            log_file_info,
            level="INFO",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )
        logger.add(
            log_file_error,
            level="ERROR",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )
        logger.add(
            log_file_warning,
            level="WARNING",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )

    def log(self, level, *args):
        frame = inspect.currentframe().f_back.f_back
        filename = inspect.getframeinfo(frame).filename
        function = inspect.getframeinfo(frame).function
        lineno = inspect.getframeinfo(frame).lineno
        logger.log(
            level,
            f"{filename}:{function}:{lineno}:Message - {''.join(str(x) for x in args)}",
        )

    def debug(self, *args):
        self.log("DEBUG", *args)

    def info(self, *args):
        self.log("INFO", *args)

    def warning(self, *args):
        self.log("WARNING", *args)

    def error(self, *args):
        self.log("ERROR", *args)

    def exception(self, *args):
        self.log("ERROR", *args)


log = LogUtil()
