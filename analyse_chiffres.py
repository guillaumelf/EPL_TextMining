# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:19:15 2017

@author: Guillaume
"""

### Import de librairies
########################

import json
import pandas as pd
import matplotlib.pyplot as plt
import re

### Définition locale de fonctions
##################################

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

### Import des données
######################

tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print('Nombre de tweets : '+str(len(tweets_data)))

### Traitement des données
##########################

tweets = pd.DataFrame()

tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data))

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

# Nettoyage et extraction des tweets en français et en anglais

english_tweets = tweets[tweets.lang=='en'].drop_duplicates()
french_tweets = tweets[tweets.lang=='fr'].drop_duplicates()
english_tweets.to_csv('tweets_en.csv',sep=';',header=True,decimal='.',encoding='utf-8',index=False) 
french_tweets.to_csv('tweets_fr.csv',sep=';',header=True,decimal='.',encoding='utf-8',index=False) 
















