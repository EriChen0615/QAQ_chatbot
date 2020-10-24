from .component import Component
from abc import ABC, abstractmethod

class NLU(Component):

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def process(self):
        raise NotImplementedError

    def do_step(self):
        self.text = self.input['text']
        self.output = self.process()
