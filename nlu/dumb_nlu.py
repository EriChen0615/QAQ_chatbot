import sys

sys.path.append('..')
from infra.nlu import NLU
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import itertools
import re

class Dumb_NLU(NLU):

    def makeErrorPartList(self):
        csvfilepath = '../data/error_keywords_1.csv'
        error_part_list = pd.read_csv(csvfilepath, sep=",", usecols=[2]).values.tolist()
        self.error_part_list = [item for sublist in error_part_list for item in sublist]


    def makeErrorList(self):
        csvfilepath = '../data/error_keywords_1.csv'
        error_list = pd.read_csv(csvfilepath, sep=",",header=None, usecols=[3]).values.tolist()
        error_list = [item for sublist in error_list for item in sublist]
        self.error_list = error_list[1:len(error_list)]

    def makeProbabilityMatrix(self):
        csvfilepath = "../data/word_error_mat.csv"
        self.probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1, 28))

    def makeKeywordList(self):
        csvfilepath = '../data/word_error_mat.csv'
        keyword_list = pd.read_csv(csvfilepath, sep=",", usecols=[0]).values.tolist()
        self.keyword_list = [item for sublist in keyword_list for item in sublist]

    def setup(self):
        print(f"{self.name} is setup")
        self.error_part_list = []
        self.error_list = []
        self.probability_matrix = []
        self.keyword_list = []

        self.makeErrorPartList()
        self.makeErrorList()
        self.makeProbabilityMatrix()
        self.makeKeywordList()

    def get_intent(self, text):
        # define yes/no
        no_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'no')))
        na_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'nah')))
        not_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'not')))
        nope_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'nope')))
        l = list(no_list) + list(na_list) + list(not_list)
        for i in l:
            if i in text:
                return 'no'
        return 'yes'

    def process(self, text):
        if not text:
            return {'error': None, 'parts': None, 'state': None}

        text = re.sub(r'[^\w\s]', '', text)

        stemmer = SnowballStemmer(language='english')
        split_text = text.split(' ')
        stemmed_text_list = []
        for word in split_text:
            stemmed_text_list.append(stemmer.stem(word.lower()))


        num_stemmed_text_list = []
        for keyword in self.keyword_list:
            if keyword in stemmed_text_list:
                num_stemmed_text_list.append(1)
            else:
                num_stemmed_text_list.append(0)

        num_stemmed_text_list = np.reshape(num_stemmed_text_list, (1, 46))

        result_list = num_stemmed_text_list.dot(self.probability_matrix)


        maximum = np.max(result_list)

        error_id = np.where(result_list == maximum)
        error_id_list = [int(item) for sublist in error_id for item in sublist]

        result_part_list = []
        result_error_list = []

        for id in error_id_list:
            result_part_list.append(self.error_part_list[id])
            result_error_list.append(self.error_list[id])

        # print(result_error_list)
        # print(result_part_list)
        intention = self.get_intent(text)
        return {'error': result_error_list, 'parts': result_part_list, 'state': intention}
        # return {'number':num, 'intent':intent}


test = Dumb_NLU()
text = ''
print(test.process(text))
