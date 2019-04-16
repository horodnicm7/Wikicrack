# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:59:26 2019

@author: Marian Horodnic
"""

import os
import time

from os import listdir, path
from config import Config

from patterns import Singleton
from logger import Logger


class Cache(object, metaclass=Singleton):
    """
        Class that implements a LRU cache to store the most recent files, just 
        to reduce the number of calls to Wikipedia and processing time.
        Also, it checks for cache integrity, given by a config file.
    """
    def __init__(self, filepath, logger):
        self.logger = logger
        self.CONF = Config(filepath, logger).get()['wikicrack']
        self.__clean_up()
        
    def flush(self):
        files = self.__get_files()
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                self.logger.log(self.__clean_up, __file__, 'File not found: ' + file)
        
        self.logger.log(self.flush, __file__, "Deleted (flush) {} files".format(len(files)))
        
    def get_file(self, subject):
        """
            Retrieves a list of files with best matching names with the given
            subject. The algorithm is empiric
        """
        files = self.__get_files(full=False)
        split_crit = ' '
        
        words = subject.split(split_crit)
        hashes = {word: 0 for word in words}
                
        index = 0
        best_score, result = -1, []
        for file in files:
            file = file[: file.rfind('.')]
            file = file[file.find('_') + 1:]
            
            if file == subject:
                result = [files[index]]
                break
            
            words = file.split(split_crit)
            occ = 0
            for word in words:
                if word in hashes:
                    occ += 1
                    
            if occ > best_score:
                result = []
                result.append(files[index])
                best_score = occ
            elif occ == best_score:
                result.append(files[index])
            
            index += 1
            
        
        # rename the resulting files to refresh accesses in cache
        path_to = self.CONF['cache']['location-windows']
        new_name = self.CONF['cache']['file-name-structure']
        for file in result:
            try:
                os.rename(path_to + file, path_to + new_name.format(
                        timestamp=int(time.time()), 
                        filename=subject
                        ))
            except:
                self.logger.log(self.get_file, __file__, 
                                "Couldn't rename: {}".format(file))
            
        return result
        
    def add_file(self, subject, content):
        """
            Creates a new file based on the given subject and adds it to cache
        """
        file = self.CONF['cache']['file-name-structure']
        path = self.CONF['cache']['location-windows']
        file = path + file.format(timestamp=int(time.time()), filename=subject)
        
        with open(file, 'wt') as f:
            f.write(content)
            f.close()
        
        self.logger.log(self.add_file, __file__, "Added: {}".format(file))
    
    def __clean_up(self):
        """
            Method that gets a list of all files from cache and deletes 
            enough files to mantain the cache limits from config
        """
        files = self.__get_files()
        
        total_size = 0
        for file in files:
            total_size += path.getsize(file)
            
        # delete the oldest files to mantain the memory limit
        max_size = self.CONF['cache']['max-size'] * 1000000 # size in MBs
        # delete the oldest files to mantain the number of files limit
        total_length = len(files)
        max_length = self.CONF['cache']['max-length']
        to_delete = []
        
        while total_size > max_size or total_length > max_length:
            total_size -= path.getsize(files[0])
            total_length -= 1
            to_delete.append(files[0])
            files.pop(0)
            
        for file in to_delete:
            try:
                os.remove(file)
            except FileNotFoundError:
                self.logger.log(self.__clean_up, __file__, 'File not found: ' + file)
                
        self.logger.log(self.__clean_up, __file__, "Deleted {} files.".format(len(to_delete)))
        
    def __get_files(self, full=True):
        """
            Returns a list of all files from cache
        """
        filepath = self.CONF['cache']['location-windows']
        raw = listdir(filepath)
        files = []
        
        for entry in raw:
            full_path = path.join(filepath, entry)
            if path.isfile(full_path):
                if full:
                    files.append(full_path)
                else:
                    files.append(entry)
                
        return files
