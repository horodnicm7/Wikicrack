# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:38:24 2019

@author: Marian Horodnic
"""

import html2text
import re

from bs4 import BeautifulSoup

from patterns import Singleton
from logger import Logger


class Decryptor(object, metaclass=Singleton):
    def __init__(self, logger):
        self.logger = logger
        
    def __clean_up(self, content):
        content = re.sub('\[[0-9a-zA-Z ]+\]', '', content)
        content = re.sub(r'^$\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[,\[\]\ ]+\n', '', content, flags=re.MULTILINE)
        
        self.logger.log(self.get_text, __file__, 
                        'Got all text from page and filtered the output')
        
        return content
    
    def set_content(self, text):
        self.soup = BeautifulSoup(text, features="lxml")
        
    def get_text(self, wrap=False):
        self.soup = self.soup.find("div", {"id": "mw-content-text"})
        content = str(self.soup.findAll("p"))
        
        self.logger.log(self.get_text, __file__, 'Filtered content from wiki')
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        h.ignore_emphasis = True
        if not wrap:
            h.body_width = 0
        return self.__clean_up(h.handle(content))
        