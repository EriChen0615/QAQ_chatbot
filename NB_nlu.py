from nlu import NLU
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import itertools
import re


class NB_NLU(NLU):

    def makeErrorPartList(self):
        csvfilepath = 'data/error_keywords_1.csv'
        error_part_list = pd.read_csv(csvfilepath, sep=",", usecols=[2]).values.tolist()
        self.error_part_list = [item for sublist in error_part_list for item in sublist]
        self.parts = set(self.error_part_list)
        # print(self.error_part_list)
        # print(len(self.error_part_list))

    def makeErrorList(self):
        csvfilepath = 'data/error_keywords_1.csv'
        error_list = pd.read_csv(csvfilepath, sep=",", header=None, usecols=[3]).values.tolist()
        error_list = [item for sublist in error_list for item in sublist]
        self.error_list = error_list[1:len(error_list)]
        # print(self.error_list)
        # print(len(self.error_list))

    def makeProbabilityMatrix(self):
        csvfilepath = "data/word_error_mat.csv"
        self.probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1, 28))
        # print(self.probability_matrix)
        # print(self.probability_matrix.shape)

    def makeKeywordList(self):
        csvfilepath = 'data/word_error_mat.csv'
        keyword_list = pd.read_csv(csvfilepath, sep=",", usecols=[0]).values.tolist()
        self.keyword_list = [item for sublist in keyword_list for item in sublist]
        # print(self.keyword_list)
        # print(len(self.keyword_list))

    def setup(self):
        # print(f"{self.name} is setup")
        self.error_part_list = []
        self.error_list = []
        self.probability_matrix = []
        self.keyword_list = []

        self.makeErrorPartList()
        self.makeErrorList()
        self.makeProbabilityMatrix()
        self.makeKeywordList()

    def get_intent(self, text):
        """
        The inital state of the dialogue needs to be set to 'no' to avoid clashing.
        intentions:
            - no
            - yes
            - greating
            - bypass
        :param text:
        :return:
        """
        # If intention yes
        yes_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'yes')))
        yeah_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'yeah')))
        yep_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'yep')))
        cheers_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'cheers')))
        yes_l = list(yes_list) + list(yeah_list) + list(yep_list) + list(cheers_list)
        for i in yes_l:
            if i in text:
                return 'yes'

        # If greating
        hi_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hi')))
        hello_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hello')))
        hey_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hello')))
        greating_l = list(hi_list) + list(hello_list) + list(hey_list)
        for i in greating_l:
            if i in text:
                return 'greating'

        return 'no'

    def get_parts(self, text):
        if re.search(r'umbrella', text.lower()) or re.search(r'magazine', text.lower()):
            return 'Tool magazine (Umbrella type)'
        elif re.search('arm', text.lower()):
            return 'Trouble Shoot (Arm type)'

    def process(self, text):

        text = text.replace(".", "")
        text = text.replace(",", "")

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
        print(result_list)

        error_id = np.argmax(result_list)


        # print(result_error_list)
        # print(result_part_list)
        intention = self.get_intent(text)
        if intention is None:
            intention = "trouble"
        return {'error': self.error_list[error_id], 'parts': self.get_parts(text), 'state': intention}
        # return {'number':num, 'intent':intent}


if __name__ == '__main__':
    test_nlu = NB_NLU()
    test_input = []
    test_output = []
    with open('test/nlu_test_input.txt', 'r') as f:
        for l in f.readlines():
            test_input.append(l.strip())
    with open('test/nlu_test_output.txt', 'r') as f:
        for l in f.readlines():
            test_output.append(l.strip().split(', '))
    #print(test_input)
    #print(test_output)
    test = NB_NLU()
    total_count = 0
    false_count = 0
    correct_count = 0
    for i in range(len(test_input)):
        print("="*20)
        print(f"Test case {i+1}")
        print(test_input[i])
        result = test.process(test_input[i])
        print("NLU output", result)
        if (result['parts'] != test_output[i][0] or result['error'] != test_output[i][1]):
                print('Expected:', test_output[i])
                false_count += 1
        else:
            print('Correct')
            correct_count += 1
        print("="*20)
        total_count += 1
    print("Success rate", correct_count/total_count)

