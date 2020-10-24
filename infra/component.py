from abc import ABC, abstractmethod

class Component(ABC):
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

