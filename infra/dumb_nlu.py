import sys

sys.path.append('..')
from infra.nlu import NLU
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import itertools

class Dumb_NLU(NLU):

    def makeErrorPartList(self):
        csvfilepath = '../data/error_keywords_1.csv'
        error_part_list = pd.read_csv(csvfilepath, sep=",", usecols=[2]).values.tolist()
        self.error_part_list = [item for sublist in error_part_list for item in sublist]
        #print(self.error_part_list)
        #print(len(self.error_part_list))

    def makeErrorList(self):
        csvfilepath = '../data/error_keywords_1.csv'
        error_list = pd.read_csv(csvfilepath, sep=",",header=None, usecols=[3]).values.tolist()
        error_list = [item for sublist in error_list for item in sublist]
        self.error_list = error_list[1:len(error_list)]
        #print(self.error_list)
        #print(len(self.error_list))

    def makeProbabilityMatrix(self):
        csvfilepath = "../data/word_error_mat.csv"
        self.probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1, 28))
        #print(self.probability_matrix)
        #print(self.probability_matrix.shape)

    def makeKeywordList(self):
        csvfilepath = '../data/word_error_mat.csv'
        keyword_list = pd.read_csv(csvfilepath, sep=",", usecols=[0]).values.tolist()
        self.keyword_list = [item for sublist in keyword_list for item in sublist]
        #print(self.keyword_list)
        #print(len(self.keyword_list))

    def setup(self):
        #print(f"{self.name} is setup")
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
        l = list(no_list) + list(na_list) + list(not_list)
        for i in l:
            if i in text:
                return 'no'
        return 'yes'

    def process(self, text):

        text = text.replace(".","")
        text = text.replace(",","")

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
        #print(result_list.shape)


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
        if intention is None:
            intention="trouble"
        return {'error': result_error_list[0], 'parts': result_part_list[0], 'state': intention}
        # return {'number':num, 'intent':intent}


test = Dumb_NLU()
text = 'The change 4 noise milling is not working.,,,'
dict=test.process(text)
print(dict)