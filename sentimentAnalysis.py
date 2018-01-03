# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 10:14:51 2017

@author: Guillaume
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.tokenize import TweetTokenizer
import re
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import matplotlib.pyplot as plt

### Définition locale de fonctions
##################################

def get_score(tweet):
    ss = sid.polarity_scores(tweet)
    score = ss['compound']
    return score

# Quelques exemples

sentences = ['I love this game','I LOVE THIS GAME ! #TontonPat',"Think Wenger was spot on today, congratulations to the team and the manager, credit where it's due !",'The manager is fucking shit #WengerOut !',"He just parks the bus and his teams play unattractive football, just sack Mourinho already ffs I've had enough of this cunt !"]
sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
print('###########################################')

#####################################################################################################        
########################### Application sur nos tweets ##############################################
#####################################################################################################

e = ThreadPoolExecutor()
wenger = list(pd.read_csv('wenger.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho = list(pd.read_csv('mourinho.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)

# On enlève les "RT @blablabla:" à l'aide d'une expression régulière ainsi que les '\n'

regex = re.compile(r'[\n\r\t]')
wenger = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"RT",r"",tweet) for tweet in wenger]
wenger = [regex.sub(' ',tweet) for tweet in wenger]
mourinho = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"RT",r"",tweet) for tweet in mourinho]
mourinho = [regex.sub(' ',tweet) for tweet in mourinho]

# Tokenisation 1ere étape : on enlève les noms d'utilisateurs et autres @ et on regroupe en un seul paragraphe

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
wenger_tweets = list(map(lambda tweet : ' '.join(tokenizer.tokenize(tweet)),wenger))
mourinho_tweets = list(map(lambda tweet : ' '.join(tokenizer.tokenize(tweet)),mourinho))

# Extraction des scores de chaque tweet

scores_wenger = list(e.map(get_score,wenger_tweets))
scores_mourinho = list(e.map(get_score,mourinho_tweets))
print('Score moyen (écart type) pour Wenger : %.4f (%.4f)' % (np.mean(scores_wenger),np.std(scores_wenger)))
print('Score moyen (écart type) pour Mourinho : %.4f (%.4f)' % (np.mean(scores_mourinho),np.std(scores_mourinho)))

# Représentation graphique : histogramme des scores

fig=plt.figure(figsize=(13,8))
plt.hist(scores_wenger,bins=20)
plt.title('Distribution des scores de sentiments pour Arsène Wenger')
fig.savefig('Images/scoresWenger.jpg')
plt.show()

fig=plt.figure(figsize=(13,8))
plt.hist(scores_mourinho,bins=20)
plt.title('Distribution des scores de sentiments pour José Mourinho')
fig.savefig('Images/scoresMourinho.jpg')
plt.show()