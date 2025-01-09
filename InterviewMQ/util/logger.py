import logging

class Logger:

    _Initialized = False

    def __init__(self, 
                 output_file_name: str, 
                 logger_name: str = __name__,
                 level = logging.INFO
                ):
        self.logger_name = logger_name
        self.level = level
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(filename=output_file_name, level=logging.INFO)

    def log(self, message):
        print("INFO: " + self.logger_name+ ": " + message)
        self._logger.info(message)



