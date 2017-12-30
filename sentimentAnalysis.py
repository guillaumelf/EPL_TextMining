# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 10:14:51 2017

@author: Guillaume
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Quelques exemples

sentences = ['I love this game','I LOVE THIS GAME ! #TontonPat',"Think Wenger was spot on today, congratulations to the team and the manager, credit where it's due !",'The manager is fucking shit #WengerOut !',"He just parks the bus and his teams play unattractive football, just sack Mourinho already ffs I've had enough of this cunt !"]
sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
        print()