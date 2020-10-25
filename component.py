from abc import ABC, abstractmethod

class Component(ABC):
    """
    The building block of a chatbot. It can connect to other components. It does the following:
    1. Call setup() upon object creation
    2. Call do_step() upon each call to run()
    3. Pass the output of the function to the input of the connected componenet

    Any subclass should implement:
    - setup() : object initialization
    - do_step() : called upon each timestep, should use self.input to produce self.output
    """
    def __init__(self):
        self.name = self.__class__.__name__
        self.input = {}
        self.output = {}
        self.next = None
        self.setup()

    def connect(self, other):
        self.next = other

    def run(self):
        self.do_step()
        if self.next:
            self.next.input = self.output

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def do_step(self):
        raise NotImplementedError

