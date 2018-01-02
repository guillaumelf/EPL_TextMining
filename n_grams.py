# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 18:19:32 2017

@author: Guillaume
"""

from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
from nltk.corpus import stopwords
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

### Définition locale de fonctions
##################################

def sorted_dict(d):
    return sorted(d.items(), key=lambda t: t[1], reverse=True)

def build_ngrams_v2(text,n,manager):
    dico_ngrams={}
    n_grams=ngrams(text.split(),n)
    for grams in n_grams:
        valeur = " ".join(grams)
        print(valeur)
        if valeur in dico_ngrams:
            dico_ngrams[valeur] += 1
        else :
            dico_ngrams[valeur] = 1
    if n == 2:
        fic = manager+'_bigrams.txt'
    elif n == 3:
        fic = manager+'_trigrams.txt'
    else :
        fic = manager+'_quadrigrams.txt'
    del_list = []
    for k in dico_ngrams.keys():
        words = k.split(' ')
        if (words[0] in stop_words) or (words[-1] in stop_words):
            del_list.append(k)
    dico_clean = {k:v for k,v in dico_ngrams.items() if k not in del_list}
    with open(fic,"w",encoding='utf-8') as f:       
        for elem in sorted_dict(dico_clean)[:100]:
            key = elem[0]
            valeur = elem[1]
            print("\"" + key + "\" : ", valeur)
            f.write("\"" + str(key) + "\" : "+ str(valeur)+"\n")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[\,\-\;\!\?\_\:\(\)\[\]\|]",r"",text)
    text = re.sub(r"è",r"e",text)
    text = re.sub(r"é",r"e",text)
    text = re.sub(r"\n",r"",text)
    text = re.sub(r"\.",r"",text)
    text = re.sub(r"\"",r"",text)
    return text

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
paragraph_wenger = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),wenger))))
paragraph_mourinho = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),mourinho))))

stop_words = set(stopwords.words())
paragraph_wenger = clean_text(paragraph_wenger)
paragraph_mourinho = clean_text(paragraph_mourinho)

tagged = list(map(lambda word : remove_useless(word),paragraph_wenger.split(' ')))
clean_words = [word for word in tagged if word != 'useless']
txt_wenger = ' '.join(clean_words)

tagged = list(map(lambda word : remove_useless(word),paragraph_mourinho.split(' ')))
clean_words = [word for word in tagged if word != 'useless']
txt_mourinho = ' '.join(clean_words)

# Création des bigrams, trigrams et quadrigrams pour les deux managers

build_ngrams_v2(txt_wenger,2,'wenger')
build_ngrams_v2(txt_wenger,3,'wenger')
build_ngrams_v2(txt_wenger,4,'wenger')

build_ngrams_v2(txt_mourinho,2,'mourinho')
build_ngrams_v2(txt_mourinho,3,'mourinho')
build_ngrams_v2(txt_mourinho,4,'mourinho')