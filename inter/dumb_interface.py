import sys
sys.path.append('..')
from infra.user_interface import UserInterface


class ConcreteInterface(UserInterface):

    def setup(self):
        self.counter = 0
        print(f"{self.name} is setup!")

    def display(self):
        if 'response' in self.input and 'browser_action' in self.input:
            print(self.input['response'])
            print("browser action:", self.input['browser_action'])

    def read(self):
        self.counter += 1
        print(f"This is hello for the {self.counter} time")
        return {'text': f"This is hello for the {self.counter} time"}

