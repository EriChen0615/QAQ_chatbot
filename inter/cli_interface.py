import sys
from infra.user_interface import UserInterface

class CLI_Interface(UserInterface):

    def setup(self):
        pass

    def read(self):
        input_text = input(">>> ")
        self.input['text'] = input_text

    def display(self, text):
        print("QAQ\' Bot:", text)
