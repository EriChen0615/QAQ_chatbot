from .component import Component
from abc import ABC, abstractmethod

class UserInterface(Component):

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    def do_step(self):
        self.display('Hi! How can I help?')
        self.output = self.read()
        
        
    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def display(self, text):
        raise NotImplementedError

