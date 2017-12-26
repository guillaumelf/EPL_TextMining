# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:23:47 2017

@author: Guillaume
"""

### Import de librairies
########################

from nltk.tokenize import TweetTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import pandas as pd
import re

### Définition locale de fonctions
##################################

def tokenize_stopwords(texte):
    lst = []
    mots = tokenizer_mots.tokenize(texte)
    
    # elimination des mots vides
    for m in mots:
        if m.lower() not in stop_words:
            lst.append(m.lower())
    return lst   

### Import des données et pré-traitement
########################################

wenger = list(pd.read_csv('wenger.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho = list(pd.read_csv('mourinho.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)

# On enlève les "RT @blablabla:" à l'aide d'une expression régulière ainsi que les '\n'

regex = re.compile(r'[\n\r\t]')
wenger = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger]
wenger = [re.sub(r"RT",r"",tweet) for tweet in wenger]
wenger = [regex.sub('',tweet) for tweet in wenger]
mourinho = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho]
mourinho = [re.sub(r"RT",r"",tweet) for tweet in mourinho]
mourinho = [regex.sub('',tweet) for tweet in mourinho]

# Tokenisation 1ere étape : on enlève les noms d'utilisateurs et autres @ et on regroupe en un seul paragraphe

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
paragraph_wenger = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),wenger))))
paragraph_mourinho = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),mourinho))))

# Tokenisation 2eme étape : on extrait les mots en éliminant les mots vides

tokenizer_mots = RegexpTokenizer('[\s+\'\.\,\?\!();\:\"\[\]\|\&]',gaps=True)
stop_words = set(stopwords.words())

wenger_words = tokenize_stopwords(paragraph_wenger)
mourinho_words = tokenize_stopwords(paragraph_mourinho)

# Premier calcul de fréquences 

fdist = FreqDist(word.lower() for word in wenger_words)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])

fdist = FreqDist(word.lower() for word in mourinho_words)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])

# Racinisation

stemmer = PorterStemmer()
stem_wenger = list(map(lambda word : stemmer.stem(word),wenger_words))
stem_mourinho = list(map(lambda word : stemmer.stem(word),mourinho_words))

# Lemmatisation

lemmatizer = WordNetLemmatizer()
lemme_wenger = list(map(lambda word : lemmatizer.lemmatize(word,pos="v"),stem_wenger))
lemme_mourinho = list(map(lambda word : lemmatizer.lemmatize(word,pos="v"),stem_mourinho))

# Second calcul de fréquences 

fdist = FreqDist(word.lower() for word in lemme_wenger)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])

fdist = FreqDist(word.lower() for word in lemme_mourinho)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
