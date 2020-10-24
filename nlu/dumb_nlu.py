import sys
sys.path.append('..')
from infra.nlu import NLU
import re
import spacy
import numpy as np
from nltk.stem.snowball import SnowballStemmer

class Dumb_NLU(NLU):

    def setup(self):
        print(f"{self.name} is setup")

    def process(self):
        num = re.search(r'\d+', self.text).group(0)
        intent = re.search(r'hello', self.text).group(0)

        text = self.text
        text = text.replace('.',' ')
        text = text.replace(',',' ')

        nlp = spacy.load('en_core_web_sm')
        lemmatizer = nlp.vocab.morphology.lemmatizer
        stemmer = SnowballStemmer(language='english')
        stemmed_text = stemmer.stem(text.lower())

        stemmed_text_list = stemmed_text.split(' ')

        # load word_error_mat file to a matrix
        probability_matrix = np.loadtxt(open("test.csv", "rb"), delimiter=",", skiprows=1, skipcols=1)
        print(probability_matrix)

        # num_stemmed_text_list = []
        # for word in stemmed_text_list:



        return {'number':num, 'intent':intent}
