# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:05:22 2019

@author: Marian
"""

import yaml


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(object, metaclass=Singleton):
    def __init__(self, path):
        self.path = path
        
    def get(self):
        result = dict()
        with open(self.path, 'rt') as conf:
            try:
                result = yaml.safe_load(conf)
            except yaml.YAMLError as exc:
                print(exc)
                
        return result