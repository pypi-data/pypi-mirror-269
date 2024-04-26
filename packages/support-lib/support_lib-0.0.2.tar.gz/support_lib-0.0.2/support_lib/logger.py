import logging
from logging.handlers import RotatingFileHandler
import os


class Logger:

    def __init__(self, logfile, logger_level, logger_name, client):
        self.logfile = logfile
        self.logger_level = logger_level
        self.logger_name = logger_name
        self.client = client
        if os.path.isfile(logfile) is False:
            if os.path.exists(os.path.dirname(logfile)):
                pass
            else:
                os.mkdir(os.path.dirname(logfile))

    def get_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger(f'{self.client} - {self.logger_name}')
        logger.setLevel(self.logger_level)
        fh = RotatingFileHandler(self.logfile, maxBytes=500000, backupCount=10)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
