import logging

class LoggerHandler():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    def __init__(self, log_type):

        if log_type == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)

        elif log_type == 'INFO':
            self.logger.setLevel(logging.INFO)

        elif log_type == 'WARNING':
            self.logger.setLevel(logging.WARNING)

        elif log_type == 'ERROR':
            self.logger.setLevel(logging.ERROR)

        elif log_type == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)

        else:
            self.logger.setLevel(logging.INFO)

    def addStreamHandler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def addFileHanlder(self):
        file_handler = logging.FileHandler("my.log")
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def getLogger(self):
        return self.logger
