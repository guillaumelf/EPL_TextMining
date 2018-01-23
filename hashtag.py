# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:22:53 2018

@author: Pierre
"""

### Import de librairies
########################

import pandas as pd
import re
from nltk.probability import FreqDist

### Définition locale de fonctions
##################################

def extract_hashtag(tweet):
    word_list=tweet.split(' ')
    hashtag = [word for word in word_list if word.startswith('#')]
    return hashtag

### Import des données et pré-traitement
########################################
    
wenger = list(pd.read_csv('wenger.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho = list(pd.read_csv('mourinho.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)

# On enlève les "RT @blablabla:" à l'aide d'une expression régulière ainsi que les '\n'

regex = re.compile(r'[\n\r\t]')
wenger = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"RT",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"è",r"e",tweet) for tweet in wenger]
wenger = [regex.sub(' ',tweet) for tweet in wenger]
mourinho = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"RT",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"é",r"e",tweet) for tweet in mourinho]
mourinho = [regex.sub(' ',tweet) for tweet in mourinho]

# On procède à un premier tri : on ne garde que les tweets contenant des hashtags

hashtag_wenger = [tweet for tweet in wenger if '#' in list(tweet)]
hashtag_mourinho = [tweet for tweet in mourinho if '#' in list(tweet)]

# Puis pour chaque manager on extrait les hashatags les concernant

wenger_h = list(map(lambda tweet: extract_hashtag(tweet), hashtag_wenger))
mourinho_h = list(map(lambda tweet: extract_hashtag(tweet), hashtag_mourinho))

hash_w=[]
for elem in wenger_h:
    for el in elem:
        el = el.lower()
        if ('ars' not in el) and ('afc' not in el) :
            hash_w.append(el)

file = open('hash_freq_w.txt','w')
fdist = FreqDist(word.lower() for word in hash_w)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('###################################')
hash_m=[]
for elem in mourinho_h:
    for el in elem:
        el = el.lower()
        if ('mufc' not in el) and ('mun' not in el) :
            hash_m.append(el)
        
file = open('hash_freq_m.txt','w')
fdist = FreqDist(word.lower() for word in hash_m)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()