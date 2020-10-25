#!/usr/bin/env python
# coding: utf-8
# to be changed, matrix value incorrect


import pandas as pd
from nltk.stem.snowball import SnowballStemmer


df = pd.read_csv('error_keywords_version_2.csv')

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


data = {}

for e in df['Trouble']:
    data[e] = [0]*len(key_words)
# p_mat = pd.DataFrame({e: [0]*len(key_words) for e in df['Trouble']}, dtype=float)
p_mat = pd.DataFrame(data, dtype=float)


stemmer = SnowballStemmer(language='english')


p_mat.index = [stemmer.stem(w.lower()) for w in key_words]

# p_mat['Noise for tool changing umbrella']['nois']

len(key_words['noise'])

for w in key_words:
    for e in key_words[w]:
        p_mat[e][w] = 1/len(key_words[w])

# p_mat['Noise for tool changing umbrella']


p_mat

import seaborn as sns

hm = sns.heatmap(p_mat)
print(p_mat.shape)
p_mat.to_csv('word_error_mat.csv')
