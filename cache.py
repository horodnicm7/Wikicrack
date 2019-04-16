# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:59:26 2019

@author: Marian
"""

import os
import time

from os import listdir, path
from config import Config


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Cache(object, metaclass=Singleton):
    """
        Class that implements a LRU cache to store the most recent files, just 
        to reduce the number of calls to Wikipedia and processing time.
        Also, it checks for cache integrity, given by a config file.
    """
    def __init__(self, filepath):
        self.CONF = Config(filepath).get()['wikicrack']
        self.__clean_up()
        
    def add_file(self, subject, content):
        """
            Creates a new file based on the given subject and adds it to cache
        """
        file = self.CONF['cache']['file-name-structure']
        path = self.CONF['cache']['location-windows']
        file = path + file.format(timestamp=int(time.time()), filename=subject)
        
        with open(file, 'wt') as f:
            f.write(content)
        
        print("Added: {}".format(file))
    
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
                print('File not found: ' + file)
                
        print("Deleted {} files.".format(len(to_delete)))
        
    def __get_files(self):
        """
            Returns a list of all files from cache
        """
        filepath = self.CONF['cache']['location-windows']
        raw = listdir(filepath)
        files = []
        
        for entry in raw:
            full_path = path.join(filepath, entry)
            if path.isfile(full_path):
                files.append(full_path)
                
        return files
    
x = Cache('default.yaml')    
x.add_file('John Wayne', 'Ana are m\nere\n,pere\n si toate cele')
