# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:42:47 2019

@author: Marian
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]