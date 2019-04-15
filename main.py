# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:27:09 2019

@author: Marian
"""

import urllib.request
import requests

from urllib import robotparser
from urllib.error import URLError, HTTPError, ContentTooShortError
from time import sleep


class WikiCrack(object):
    url = 'https://www.wikipedia.org/wiki/'
    log_path = 'log.txt'
    no_attempts = 10
    start_agent = 'Wikicrack'
    
    def __init__(self):
        self.log_file = open(self.log_path, 'wt')
        pass
    
    def destructor(self):
        self.log_file.close()
    
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
    
    def _download_page(self, url, user_agent):
        self.log_file.write('Downloading: ' + url + ' ......... ')
        
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
            
            tries += 1
        return page
    
    def search_for(self, term):
        keywords = term.split(' ')
        agent = self.get_valid_user_agent()
        content = self._download_page(self.url + keywords[0], agent)
        # TODO: ca sa obtii link-ul pe care esti acum, wikipedia are 
        # ceva in header pentru asta (cauta pe un exemplu)
        return content

if __name__ == "__main__":
    bot = WikiCrack()
    print(bot.search_for('John'))
    bot.destructor()
        
    
    
    
    
    
    
    
    