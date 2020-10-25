from abc import ABC, abstractmethod
from .component import Component

class Tracker(Component):

    def setup(self):
        print("Tracker is setup")
        self.state = {'cur_intent':None, 'number':None}
        self.slots = {}

    def do_step(self):
        self.update_state()
        self.output = self.state

    def update_state(self):
        self.state['cur_intent'] = self.input['intent'] if 'intent' in self.input else 'init'
        self.state['number'] = self.input['number'] if 'number' in self.input else 0
        self.state['response'] = f"This is round {self.state['number']} and the intent is {self.state['cur_intent']}"

