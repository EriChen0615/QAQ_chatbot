import sys
sys.path.append('..')
from infra.nlu import NLU
import re
import spacy
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer

class Dumb_NLU(NLU):

    def setup(self):
        print(f"{self.name} is setup")

    def process(self):
        # num = re.search(r'\d+', self.text).group(0)
        # intent = re.search(r'hello', self.text).group(0)

        text = self.text
        text = text.replace('.',' ')
        text = text.replace(',',' ')

        nlp = spacy.load('en_core_web_sm')
        lemmatizer = nlp.vocab.morphology.lemmatizer
        stemmer = SnowballStemmer(language='english')
        stemmed_text = stemmer.stem(text.lower())

        stemmed_text_list = stemmed_text.split(' ')

        # load word_error_mat file to a matrix
        csvfilepath = "../data/word_error_mat.csv"
        probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1,28))
        # print(probability_matrix)

        keyword_list = pd.read_csv(csvfilepath, sep=",",usecols=[0]).values.tolist()
        print(keyword_list)

        num_stemmed_text_list = []
        for word, keyword in stemmed_text_list, keyword_list:
            if word == keyword:
                num_stemmed_text_list.append(1)
            else:
                num_stemmed_text_list.append(0)

        print(num_stemmed_text_list)


        # return {'number':num, 'intent':intent}


test = Dumb_NLU()
test.text = 'The change 4 noise milling is not working.,,,'
test.process()