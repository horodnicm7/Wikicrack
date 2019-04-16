# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:05:22 2019

@author: Marian Horodnic
"""

import yaml

from patterns import Singleton
from logger import Logger


class Config(object, metaclass=Singleton):
    def __init__(self, path, logger):
        self.path = path
        self.logger = logger
        
    def get(self):
        result = dict()
        with open(self.path, 'rt') as conf:
            try:
                result = yaml.safe_load(conf)
            except yaml.YAMLError as exc:
                self.logger.log(self.get, __file__, exc)
                
        return result
