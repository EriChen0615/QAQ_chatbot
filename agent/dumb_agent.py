import sys
sys.path.append('..')
from infra.agent import Agent

class DumbAgent(Agent):

    def setup(self):
        print(f"{self.name} is setup")

    def step(self, state):
        return {'bot_intent':'respond', 'response': f"intent: {state['cur_intent']} at round {state['number']}"}

