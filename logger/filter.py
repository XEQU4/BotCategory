import logging


class SkipApscheduler(logging.Filter):
    def filter(self, record):
        return \
                not record.msg.startswith('Looking for jobs to run') and \
                not record.msg.startswith('Next wakeup is due') and \
                not record.msg.startswith('Removed job') and \
                not record.msg.startswith('Added job') and \
                not record.msg.startswith('Job') and \
                not record.msg.startswith('Run time of job') and \
                not record.msg.startswith('Running job')


class CustomFormatterConsole(logging.Formatter):
    """Logging filter to Console handler"""

    green = "\x1b[38;5;48m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    back_grey = "\x1b[38;5;7m"
    cyan = "\x1b[38;5;14m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [pathname: %(pathname)s] - [function: %(funcName)s] - [line: %(lineno)d]\n\t%(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: cyan + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + back_grey + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class CustomFormatterFile(logging.Formatter):
    """Logging filter to File handler"""

    format = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [function: %(funcName)s] - [%(message)s]"
    datefmt = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
