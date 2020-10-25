from abc import ABC, abstractmethod
from .component import Component

class Agent(Component):
    """
    Base class for agents. It receives a state from the previous component and product an action.

    Input:
        - state :dict

    Output:
        - action
    """

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
