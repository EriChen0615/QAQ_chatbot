import sys
sys.path.append('..')

from nltk import PorterStemmer
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
        text = text.replace(".","")
        text = text.replace(",","")

        # nlp = spacy.load('en_core_web_sm')
        # lemmatizer = nlp.vocab.morphology.lemmatizer
        stemmer = SnowballStemmer(language='english')
        split_text = text.split(' ')
        stemmed_text_list = []
        for word in split_text:
            stemmed_text_list.append(stemmer.stem(word.lower()))

        # load word_error_mat file to a matrix
        csvfilepath = "../data/word_error_mat.csv"
        probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1,28))

        error_list = pd.read_csv(csvfilepath, sep=",",header=None, nrows=1).values.tolist()
        error_list = [item for sublist in error_list for item in sublist]
        error_list = error_list[1:len(error_list)]
        keyword_list = pd.read_csv(csvfilepath, sep=",",usecols=[0]).values.tolist()
        flat_keyword_list = [item for sublist in keyword_list for item in sublist]

        num_stemmed_text_list = []
        for keyword in flat_keyword_list:
            if keyword in stemmed_text_list:
                num_stemmed_text_list.append(1)
            else:
                num_stemmed_text_list.append(0)

        num_stemmed_text_list = np.reshape(num_stemmed_text_list, (1, 46))

        result_list = num_stemmed_text_list.dot(probability_matrix)


        maximum = np.max(result_list)

        error_id = np.where(result_list == maximum)
        error_id_list = [int(item) for sublist in error_id for item in sublist]

        result_error_list = []

        for id in error_id_list:
            result_error_list.append(error_list[id])

        # print(result_error_list)
        return result_error_list
        # return {'number':num, 'intent':intent}


# test = Dumb_NLU()
# test.text = 'The change 4 noise milling is not working.,,,'
# test.process()