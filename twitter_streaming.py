# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:46:46 2017

@author: Guillaume
"""

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = 'MY-CONSUMER-KEY'
consumer_secret = 'My-CONSUMER-SECRET'
access_token = 'MY-ACCESS-TOKEN'
access_secret = 'MY-ACCESS-SECRET'

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

    #This line filters Twitter Streams to capture data by the keywords: the names of the two managers
    stream.filter(track=['wenger','mourinho'])
    
