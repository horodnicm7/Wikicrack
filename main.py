# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:27:09 2019

@author: Marian Horodnic
"""

import urllib.request

from urllib import robotparser
from urllib.error import URLError, HTTPError, ContentTooShortError
from time import sleep

from config import Config
from logger import Logger
from decryptor import Decryptor
from cache import Cache


class WikiCrack(object):
    url = 'https://www.wikipedia.org/wiki/'
    
    def __init__(self):
        self.logger = Logger('.\\logs\\')
        self.CONF = Config('default.yaml', self.logger).get()['wikicrack']
        self.no_attempts = self.CONF['crawler']['max-attempts-download']
        self.start_agent = self.CONF['crawler']['agent-name']
        self.sleep_for = self.CONF['crawler']['sleep-between']
        self.max_accepted = self.CONF['cache']['limit-per-subject']
        self.accepted_length = self.CONF['output']['min-accepted-length']
        self.word_wrap = self.CONF['output']['word-wrap']
        self.decrypt = Decryptor(self.logger)
        self.cache = Cache(self.CONF, self.logger)
        self.agent = None
    
    def get_valid_user_agent(self):
        # init the robots.txt parser
        parser = robotparser.RobotFileParser()
        parser.set_url(self.url + '/robots.txt')
        parser.read()
            
        # trying to get a valid agent name in less than 10 attempts
        user_agent = self.start_agent
        no_hops = 0
        while not parser.can_fetch(user_agent, self.url):
            if user_agent[-1].isdigit():
                user_agent = user_agent[:-1] + str(int(user_agent[-1]) + 1)
            else:
                user_agent = user_agent + '1'
                
            no_hops += 1
            # error in finding a valid name
            if no_hops > 9:
                return 'default-agent'
                    
        return user_agent
    
    def __download_page(self, url, user_agent):
        self.logger.log(self.__download_page, __file__,
                        'Downloading: ' + url + ' ...')
        
        page = None
        req = urllib.request.Request(url)
        req.add_header('User-agent', user_agent)
        
        tries = 0
        while tries < self.no_attempts:
            try:
                response = urllib.request.urlopen(req)
                page = response.read().decode('utf-8')
                break
            except (URLError, HTTPError, ContentTooShortError) as e:
                if hasattr(e, 'code'):
                    if not (e.code >= 500 and e.code < 600):
                        return None
                sleep(self.sleep_for)
            tries += 1
        return page    
    
    def search_for(self, term):
        self.logger.log(self.search_for, __file__, 
                        "Searching for subject: {}...".format(term))
        hits = self.cache.get_file(term)
        
        if hits == [] or len(hits) > self.max_accepted:
            # if there are no cache hits
            if not hits:
                self.logger.log(self.search_for, __file__, 
                                'Cache miss!')
            
            # check if the search term is too general for our cache
            if len(hits) > self.max_accepted:
                self.logger.log(self.search_for, __file__, 
                                'Too many cache hits! Considering it as a wrong result')
            keywords = term.split(' ')
            
            if not self.agent:
                self.agent = self.get_valid_user_agent()
            content = self.__download_page(self.url + keywords[0], self.agent)

            # prepare decryptor and get clean text from it
            self.decrypt.set_content(content)
            result = self.decrypt.get_text(wrap=self.word_wrap)
            
            # check if the text's length is reasonable
            if len(result) >= self.accepted_length:
                # add entry in cache
                self.cache.add_file(term, result)
                return result
            else:
                # content is too short and it's a great chance that we're on the  
                # 'may also refer to' page
                self.logger.log(self.search_for, __file__, 
                            'Content too short! Considering the search operation a failure.')
                return ""
        else:
            self.logger.log(self.search_for, __file__, 
                            'Cache hit! Extracting from cache...')
            with open(hits[0], 'rt') as file:
                return file.read()


if __name__ == "__main__":
    bot = WikiCrack()
    bot.search_for('Dwayne_Johnson')
    bot.search_for('Michael_Jackson')
    bot.search_for('Kevin_Hart')
    bot.search_for('Tom_Cruise')
