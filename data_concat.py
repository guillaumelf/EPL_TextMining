# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 13:40:42 2017

@author: Guillaume
"""

### Import de librairies
########################

import json
import glob
from functools import reduce

### Définition locale de fonctions
##################################

def add_tweets(file):
    tweets_file = open(file, "r")
    tweets_data = []
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    return tweets_data

def split_list(l1,l2):
    return [d for d in l1]+[d for d in l2]
 
### Import des données et pré-traitement
########################################

files = glob.glob('twitter_data*.txt')

mapped_values = map(add_tweets,files)
tweets = reduce(split_list,mapped_values)

with open('twitter_data.txt', 'w',encoding='utf-8') as outfile:
    for tweet in tweets:
        json.dump(tweet, outfile)
        print('Line dumped successfully !')
