from component import Component
from abc import ABC, abstractmethod

class NLU(Component):
    """
    Base class for Natural Language Understanding componenet. It receieves text from the previous component and produce intent/entity

    Input:
        - text :str

    Output:
        - intent :str
        - entity :dict

    Any subclass should implement:
        - setup(): initialization
        - process(): conduct Named Entity Recognition (NER) to extract intent and entities from text
    """

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def process(self, text):
        raise NotImplementedError

    def do_step(self):
        self.text = self.input['text']
        self.output = self.process(text)
