# A Reddit bot that posts explanation of xkcd comic strips posted in comments
# The explanation is extracted from http://explainxkcd.com
# Created by Ayush Dwivedi (/u/kindw)
# License: MIT License

from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = 'commented.txt'
# Location of file where id's of already visited comments are maintained

header = '**Current word of the day:**\n'
footer = '\n*---This definition was extracted from [dictionary.com] | Bot created by u/EatsPi | [Source code]()*'
# Text to be posted along with comic description


def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('WotdBot', user_agent = 'web:WotdBot:v0.1 (by /u/EatsPi)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetchdata(url):
    r = requests.get(url)
    print('Current URL:' + url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = ''
    wotdurl = ''

    while "wordoftheday" not in currentTag:
        currentTag = link.get('href') 
        print(currentTag)
        url = url+currentTag
        print(url)
        #r = requests.get(url)
        #soup = BeautifulSoup(r.content, 'html.parser')
        
        #link.find(class="wotdHolder_word")
        #wotdurl = link.get('href')

    print(title + '<- Title')
    wotd = title.split(" ", 1)

    print(wotd + '<-Wotd')
  
    return data


def run_wotdbot(reddit):
    
    print("Getting 250 comments...\n")
    
    for comment in reddit.subreddit('test').comments(limit = 250):
        match = re.findall('wotd', comment.body)
        if match:
            print("Request found in comment with comment ID: " + comment.id)
            print(comment.body) #testing the comment body contents
            myurl = 'http://www.dictionary.com'
            file_obj_r = open(path,'r')
            
            
            try:
                explanation = fetchdata(myurl)
            except:
                print('Fetch has failed...\n')
                # Typical cause for this will be a URL for an xkcd that does not exist (Example: https://www.xkcd.com/772524318/)
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting the word of the day\n')
                    #comment.reply(header + explanation + footer)
                    
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
            
            print("Completed.")
            time.sleep(5)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_wotdbot(reddit)


if __name__ == '__main__':
    main()