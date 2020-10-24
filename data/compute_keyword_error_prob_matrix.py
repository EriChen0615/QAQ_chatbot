#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import spacy
import nltk
from nltk.stem.snowball import SnowballStemmer

from nltk.stem.porter import *

df = pd.read_csv('error_kws.csv')

df

key_words = {}

df['Key_word'][0].split(', ')

for index, row in df.iterrows():
    for w in row['Key_word'].split(', '):
        if w in key_words:
            key_words[w].add(row['Trouble'])
        else:
            key_words[w] = {row['Trouble']}
key_words

p_mat = pd.DataFrame({e: [0]*len(key_words) for e in df['Trouble']}, dtype=float)

nlp = spacy.load('en_core_web_sm')
lemmatizer = nlp.vocab.morphology.lemmatizer

stemmer = SnowballStemmer(language='english')
# stemmer = PorterStemmer()

p_mat.index = [stemmer.stem(w.lower()) for w in key_words]

p_mat['Noise for tool changing']['nois']

len(key_words['noise'])

for w in key_words:
    for e in key_words[w]:
        p_mat[e][w] = 1/len(key_words[w])

p_mat['Noise for tool changing']


p_mat

import seaborn as sns

hm = sns.heatmap(p_mat)

p_mat.to_csv('word_error_mat.csv')
