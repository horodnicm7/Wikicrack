# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:05:22 2019

@author: Marian
"""

import yaml


class Config(object):
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