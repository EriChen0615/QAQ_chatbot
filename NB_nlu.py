from nlu import NLU
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import itertools
import re



class NB_NLU(NLU):

    error_probability_threshold = 0.75

    def makeErrorPartList(self):
        csvfilepath = 'data/error_keywords_1.csv'
        error_part_list = pd.read_csv(csvfilepath, sep=",", usecols=[2]).values.tolist()
        self.error_part_list = [item for sublist in error_part_list for item in sublist]
        self.parts = set(self.error_part_list)

    def makeErrorList(self):
        csvfilepath = 'data/error_keywords_1.csv'
        error_list = pd.read_csv(csvfilepath, sep=",", header=None, usecols=[3]).values.tolist()
        error_list = [item for sublist in error_list for item in sublist]
        self.error_list = error_list[1:len(error_list)]

    def makeProbabilityMatrix(self):
        csvfilepath = "data/word_error_mat.csv"
        self.probability_matrix = np.loadtxt(open(csvfilepath, "rb"), delimiter=",", skiprows=1, usecols=range(1, 28))

    def makeKeywordList(self):
        csvfilepath = 'data/word_error_mat.csv'
        keyword_list = pd.read_csv(csvfilepath, sep=",", usecols=[0]).values.tolist()
        self.keyword_list = [item for sublist in keyword_list for item in sublist]

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

    def textPreprocess(self,text):

        text_without_punctuation = re.sub(r'[^\w\s]', '', text)
        stemmer = SnowballStemmer(language='english')
        split_text = text_without_punctuation.split(' ')
        stemmed_text_list = []
        for word in split_text:
            stemmed_text_list.append(stemmer.stem(word.lower()))

        return stemmed_text_list

    def get_intent(self, text):
        """
        The inital state of the dialogue needs to be set to 'no' to avoid clashing.
        intentions:
            - no
            - yes
            - greeting
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

        # If greeting
        hi_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hi')))
        hello_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hello')))
        hey_list = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'hello')))
        greeting_l = list(hi_list) + list(hello_list) + list(hey_list)
        for i in greeting_l:
            if i in text:
                return 'greeting'

        return 'no'

    def get_parts(self, text):
        if re.search(r'umbrella', text.lower()) or re.search(r'magazine', text.lower()):
            return 'Tool magazine (Umbrella type)'
        elif re.search('arm', text.lower()):
            return 'Trouble Shoot (Arm type)'

    def process(self, text):

        if text.startswith('$') and text.startswith('$'):
            text = text.replace('$',' ')
            intention = 'solution'
            return {'solution': text, 'state': intention}

        stemmed_text_list = self.textPreprocess(text)
        intention = self.get_intent(text)
        num_stemmed_text_list = []
        for keyword in self.keyword_list:
            if keyword in stemmed_text_list:
                num_stemmed_text_list.append(1)
            else:
                num_stemmed_text_list.append(0)

        num_stemmed_text_list = np.reshape(num_stemmed_text_list, (1, 46))

        result_list = num_stemmed_text_list.dot(self.probability_matrix)
        print(result_list)

        error_id = None
        if np.argmax(result_list) >= self.error_probability_threshold:
             error_id = np.argmax(result_list)

        if not intention:
            intention = "trouble"

        if error_id:
            return {'error': self.error_list[error_id], 'parts': self.get_parts(text), 'state': intention}

        return {'error': None, 'parts': None, 'state': intention}


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


