import logging
import sys
import daiquiri

class QueryLogger(object):
    def __init__(self, file_path):
        daiquiri.setup(level=logging.INFO, outputs=(
            daiquiri.output.Stream(sys.stdout),
            daiquiri.output.File(file_path)
        ))
        self.logger = daiquiri.getLogger(__name__, subsystem="Queries")

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)
