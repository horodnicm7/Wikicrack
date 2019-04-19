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


class WikiCrack(object):
    url = 'https://www.wikipedia.org/wiki/'
    
    def __init__(self):
        self.logger = Logger('.\\logs\\')
        self.CONF = Config('default.yaml', self.logger).get()['wikicrack']
        self.no_attempts = self.CONF['crawler']['max-attempts-download']
        self.start_agent = self.CONF['crawler']['agent-name']
        self.sleep_for = self.CONF['crawler']['sleep-between']
        pass
    
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
        keywords = term.split(' ')
        agent = self.get_valid_user_agent()
        print(agent)
        content = self.__download_page(self.url + keywords[0], agent)
        # TODO: ca sa obtii link-ul pe care esti acum, wikipedia are 
        # ceva in header pentru asta (cauta pe un exemplu)
        return content

if __name__ == "__main__":
    bot = WikiCrack()
    print(bot.search_for('Michael_Jackson'))
        
    
    
    
    
    
    
    
    