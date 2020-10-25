import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import nltk
from nltk.corpus import stopwords
import itertools
import re
from NB_nlu import NB_NLU

def read_manual():
    p = input('please enter your manual path here >>> ')
    manual_df = pd.read_csv(p)
    return manual_df

def process_manual(df):
    """part, error description, solution"""
    df_error_des = df['error description'].values.tolist()
    for er in df_error_des:
        er = er.split()
        er = [re.sub('\W+','', i) for i in er]
        er = [i for i in er if i not in stopwords.words('english')]
    df['error description'] = df_error_des

if __name__ == '__main__':
    manual = read_manual()
    process_manual(manual)
    manual.to_csv('data/error_keywords_1.csv')