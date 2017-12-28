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
from concurrent.futures import ThreadPoolExecutor

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

list_allowed = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','£','0','1','2','3','4','5','6','7','8','9','10']
def remove_useless(word):
    useful = 0
    letters = list(word)
    for elem in list_allowed :
        if elem in letters :
            useful +=1
    if useful == 0 :
        new_word = 'useless'
    else :
        new_word = word
    return new_word
                  
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
e = ThreadPoolExecutor()
wenger_words = e.map(remove_useless,tokenize_stopwords(paragraph_wenger))
wenger_words = [word for word in wenger_words if word != 'useless']
mourinho_words = e.map(remove_useless,tokenize_stopwords(paragraph_mourinho))
mourinho_words = [word for word in mourinho_words if word != 'useless']

# Premier calcul de fréquences 

fdist = FreqDist(word.lower() for word in wenger_words)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
print('#################################################')
fdist = FreqDist(word.lower() for word in mourinho_words)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
print('#################################################')

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
print('#################################################')
fdist = FreqDist(word.lower() for word in lemme_mourinho)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])