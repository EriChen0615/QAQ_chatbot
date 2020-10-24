import sys
sys.path.append('..')
from infra.nlu import NLU
import re

class Dumb_NLU(NLU):

    def setup(self):
        print(f"{self.name} is setup")

    def process(self):
        num = re.search(r'\d+', self.text).group(0)
        intent = re.search(r'hello', self.text).group(0)
        return {'number':num, 'intent':intent}
