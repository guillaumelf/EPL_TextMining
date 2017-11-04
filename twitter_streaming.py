# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:46:46 2017

@author: Guillaume
"""

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = 'zOGQ2hg92J0pFbKq9vFg2U57x'
consumer_secret = '9p5ABXZ2hc3EqklGY59CgdVxGG9AVZLR7ODo7zePsg76OGnYWh'
access_token = '275977750-0mt28ljghdDRFfF4ZGHu1CZwl6adtPvMMwMRRS7p'
access_secret = 'csBQf2KPKvf8a4Cff2yiPa1Wu12qMr2UMVepCHiKzuRK7'

#This is an advanced listener that prints received tweets to stdout and writes them in a file.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        try:
            with open('twitter_data.txt', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
    
if __name__ == '__main__':

    #This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: the names of the 'Big 6' managers
    stream.filter(track=['wenger','guardiola','mourinho','klopp','pochettino','conte'])
    
