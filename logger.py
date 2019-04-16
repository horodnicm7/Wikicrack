# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:40:34 2019

@author: Marian
"""
import time
import datetime
import os

from patterns import Singleton


class Logger(object, metaclass=Singleton):
    def __init__(self, path):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        self.path = path + 'log_' + str(timestamp) + '.txt'
        self.file = open(self.path, 'wt')
        
    def log(self, function, script, message):
        self.file.write("[{0} in {1}]: {2}\n".format(function, os.path.basename(script), message))
        self.file.flush()
        
    def __del__(self):
        self.file.close()
