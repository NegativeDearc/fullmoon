# -*- coding:utf-8 -*-
import os
import logging
from app import app


class AppLog(object):
    def __init__(self):
        # os.pardir -> parent directory
        self.__log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/logs/log.txt'
        self.handler = logging.FileHandler(self.__log_path)
        self.formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        # settings
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(logging.DEBUG)


class DebugFalseLog(AppLog):
    def __init__(self):
        super(DebugFalseLog, self).__init__()
        self.formatter = app.debug_log_format
        self.handler.setLevel(logging.ERROR)

    def get_handler(self):
        return self.handler