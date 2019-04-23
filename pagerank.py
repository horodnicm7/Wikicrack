# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 22:26:34 2019

@author: Marian Horodnic
"""

from patterns import Singleton
from logger import Logger
from base import Summary

class PageRank(Summary, metaclass=Singleton):
    def __init__(self, logger, conf):
        super(PageRank, self).__init__(logger, conf)
        
    def sumarize(self, text):
        self.text = text
        