# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:36:18 2018

@author: Guillaume
"""

### Import de librairies
########################

from nltk.tokenize import TweetTokenizer, word_tokenize
import pandas as pd
import re
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from concurrent.futures import ThreadPoolExecutor

### Définition locale de fonctions
##################################  

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

wenger_pos = list(pd.read_csv('wenger_positive.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho_pos = list(pd.read_csv('mourinho_positive.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
wenger_neg = list(pd.read_csv('wenger_negative.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)
mourinho_neg = list(pd.read_csv('mourinho_negative.csv',sep=';',header=0,decimal='.',encoding='utf-8').text)

# On enlève les "RT @blablabla:" à l'aide d'une expression régulière ainsi que les '\n'

regex = re.compile(r'[\n\r\t]')
wenger_pos = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger_pos]
wenger_pos = [re.sub(r"RT",r"",tweet) for tweet in wenger_pos]
wenger_pos = [re.sub(r"è",r"e",tweet) for tweet in wenger_pos]
wenger_pos = [regex.sub(' ',tweet) for tweet in wenger_pos]
wenger_neg = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in wenger_neg]
wenger_neg = [re.sub(r"RT",r"",tweet) for tweet in wenger_neg]
wenger_neg = [re.sub(r"è",r"e",tweet) for tweet in wenger_neg]
wenger_neg = [regex.sub(' ',tweet) for tweet in wenger_neg]
mourinho_pos = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho_pos]
mourinho_pos = [re.sub(r"RT",r"",tweet) for tweet in mourinho_pos]
mourinho_pos = [re.sub(r"è",r"e",tweet) for tweet in mourinho_pos]
mourinho_pos = [regex.sub(' ',tweet) for tweet in mourinho_pos]
mourinho_neg = [re.sub(r"RT @(.*?):",r"",tweet) for tweet in mourinho_neg]
mourinho_neg = [re.sub(r"RT",r"",tweet) for tweet in mourinho_neg]
mourinho_neg = [re.sub(r"è",r"e",tweet) for tweet in mourinho_neg]
mourinho_neg = [regex.sub(' ',tweet) for tweet in mourinho_neg]

# Tokenisation 1ere étape : on enlève les noms d'utilisateurs et autres @ et on regroupe en un seul paragraphe

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
paragraph_wenger_pos = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),wenger_pos))))
paragraph_wenger_neg = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),wenger_neg))))
paragraph_mourinho_pos = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),mourinho_pos))))
paragraph_mourinho_neg = ' '.join(map(lambda tweet : ' '.join(tweet),list(map(lambda tweet : tokenizer.tokenize(tweet),mourinho_neg))))

# Etiquetage grammatical

wenger_tags_pos = pos_tag(word_tokenize(paragraph_wenger_pos))
wenger_tags_neg = pos_tag(word_tokenize(paragraph_wenger_neg))
mourinho_tags_pos = pos_tag(word_tokenize(paragraph_mourinho_pos))
mourinho_tags_neg = pos_tag(word_tokenize(paragraph_mourinho_neg))

e = ThreadPoolExecutor()

# Extraction des adjectifs et nettoyage

wenger_pos_jj = [word[0].lower() for word in wenger_tags_pos if word[1] == 'JJ']
wenger_pos_jj = e.map(remove_useless,remove_useless(wenger_pos_jj))
wenger_pos_jj = [word for word in wenger_pos_jj if word != 'useless']

wenger_neg_jj = [word[0].lower() for word in wenger_tags_neg if word[1] == 'JJ']
wenger_neg_jj = e.map(remove_useless,remove_useless(wenger_neg_jj))
wenger_neg_jj = [word for word in wenger_neg_jj if word != 'useless']

mourinho_pos_jj = [word[0].lower() for word in mourinho_tags_pos if word[1] == 'JJ']
mourinho_pos_jj = e.map(remove_useless,remove_useless(mourinho_pos_jj))
mourinho_pos_jj = [word for word in mourinho_pos_jj if word != 'useless']

mourinho_neg_jj = [word[0].lower() for word in mourinho_tags_neg if word[1] == 'JJ']
mourinho_neg_jj = e.map(remove_useless,remove_useless(mourinho_neg_jj))
mourinho_neg_jj = [word for word in mourinho_neg_jj if word != 'useless']

# L'étiquetage n'est pas parfait, certains mots sont considérés comme des adjectifs alors qu'ils ne le sont pas : on les 
# élimine "à la main" en créant une liste d'indésirables

indes_wenger = ['own','arsenal','2-2','many','much','same','referee','other','such','wenger','only','next','suicide','ll','fuck','arsene','afc','farcical','re','ve','fucking','derby','tonight','whole','2-3','1-1','4-0','current','potential','double','crystal','lol','wish','able','810th','3-2','further','year-old','vs','victory','3-1']
indes_mourinho = ['manutd','able','mourinho','same','much','other','next','mufc','many','derby','jose','enough','such','only','second','pre-manchester','2-2','re','2-0','ve','whole','arsenal','anti','utd','martial','due','ll','absolute','further','dive','half','fuck','league','utter','duncan','current','double','vs','4-2','isn','rid','lol','3-1','th']

# Calcul des fréquences pour les adjectifs

file = open('wenger_adj_pos.txt','w')
fdist = FreqDist(word.lower() for word in wenger_pos_jj if len(word) > 1 and word.lower() not in indes_wenger)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')
file = open('wenger_adj_neg.txt','w')
fdist = FreqDist(word.lower() for word in wenger_neg_jj if len(word) > 1 and word.lower() not in indes_wenger)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')
file = open('mourinho_adj_pos.txt','w')
fdist = FreqDist(word.lower() for word in mourinho_pos_jj if len(word) > 1 and word.lower() not in indes_mourinho)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')
file = open('mourinho_adj_neg.txt','w')
fdist = FreqDist(word.lower() for word in mourinho_neg_jj if len(word) > 1 and word.lower() not in indes_mourinho)
most_common = fdist.most_common(100)
for i in range(len(most_common)):
    if most_common[i][1] > 1:
        print(most_common[i])
        file.write("{}:{}\n".format(most_common[i][0],most_common[i][1]))
file.close()
print('#################################################')