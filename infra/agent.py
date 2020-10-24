from abc import ABC, abstractmethod
from .component import Component

class Agent(Component):

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def step(self):
        raise NotImplementedError

    def do_step(self):
        self.state = self.input
        self.action = self.step(self.state)
        self.output = self.action
