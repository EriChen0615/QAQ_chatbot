from .component import Component
from .tracker import Tracker
from .agent import Agent

class DialogueManager(Component):

    def __init__(self, tracker, agent):
        super().__init__()
        self.tracker = tracker
        self.agent = agent
        self.tracker.connect(agent)

    def setup(self):
        print("Dialogue Manager is setup!")

    def do_step(self):
        self.tracker.input = self.input
        self.tracker.run()
        self.agent.run()
        self.output = self.to_front(self.agent.output)

    def to_front(self, action):
        return {'response':action['response'], 'browser_action':'reply'}


