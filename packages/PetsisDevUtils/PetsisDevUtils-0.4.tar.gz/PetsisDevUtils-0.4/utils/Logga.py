import logging


def log(mess, level='INFO'):
    Logga().log(mess, level)
def dlog(mess):
    log(mess, level='DEBUG')


class Logga:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logga, cls).__new__(cls)
            handler = logging.StreamHandler()
            handler.setFormatter(CustomFormatter())
            logger = logging.getLogger("my_logger")
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)  # Set desired logging level
            logger.propagate = False
            cls._instance.logga = logger
            cls._instance.log(mess='Logga.__init__')
        return cls._instance
    def log(self, mess: str, level='INFO'):
        level_lib = {
            'INFO': self.logga.info,
            'DEBUG': self.logga.debug,
            'WARNING': self.logga.warning,
            'ALERT': self.logga.warning,
            'ERROR': self.logga.error,
            'CRITICAL': self.logga.critical
        }
        level_lib[level](mess)


class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: "\033[94m#%(levelname)s:%(message)s\033[0m",  # Blue
        logging.INFO: "\033[92m#%(levelname)s:%(message)s\033[0m",  # Green
        logging.WARNING: "\033[93m#%(levelname)s:%(message)s\033[0m",  # Yellow
        logging.ERROR: "\033[91m#%(levelname)s:%(message)s\033[0m",  # Red
        logging.CRITICAL: "\033[101m#%(levelname)s:%(message)s\033[0m",  # Bright red
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)
