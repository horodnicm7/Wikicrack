# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:40:34 2019

@author: Marian Horodnic
"""
import time
import datetime
import os

from patterns import Singleton


class Logger(object, metaclass=Singleton):
    logs_limit = 5
    def __init__(self, path):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        self.path = path
        self.filename = path + 'log_' + str(timestamp) + '.txt'
        self.file = open(self.filename, 'wt')
        self.__clean_up()
        
    def log(self, function, script, message):
        self.file.write("[{0} in {1}]: {2}\n".format(function, os.path.basename(script), message))
        self.file.flush()
        
    def __clean_up(self):
        raw = os.listdir(self.path)
        files = []
        
        for entry in raw:
            full_path = os.path.join(self.path, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
                
        no_deleted = 0
        while len(files) > self.logs_limit:
            try:
                os.remove(files[0])
                no_deleted += 1
            except:
                self.log(self.__clean_up, __file__,
                         "Couldn't delete log file: {}".format(files[0]))
            files.pop(0)
            
        self.log(self.__clean_up, __file__, 
                 "Deleted {} log files.".format(no_deleted))
                    
    def __del__(self):
        self.file.close()
