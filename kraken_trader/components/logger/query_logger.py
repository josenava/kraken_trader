import logging
import sys

class QueryLogger(object):
    def __init__(self, logger, file_path):
        self.logger = logger
        # create file handler which logs even debug messages
        fh = logging.FileHandler(file_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)
