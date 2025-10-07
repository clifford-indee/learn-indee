import logging
import time

class Logger():
    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logger.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        cur_time = time.struct_time("%y-%m-%d")

        # log file
        self.LogFileName = '..\\logs\\log'+cur_time+'.txt'
        file_handler = logging.FileHandler(self.LogFileName, mode='a')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_level)
        self.logger.addHandler(file_handler)