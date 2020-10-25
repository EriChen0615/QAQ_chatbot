from infra.chatbot import Chatbot
from inter.dumb_interface import ConcreteInterface
from nlu.dumb_nlu import Dumb_NLU
from agent.dumb_agent import DumbAgent
from infra.tracker import Tracker
from infra.dialogue_manager import DialogueManager

if __name__ == '__main__':
    interface = ConcreteInterface()
    nlu = Dumb_NLU()
    dm = DialogueManager(Tracker(), DumbAgent())
    dumb_bot = Chatbot([interface, nlu, dm])
    dumb_bot.step(10)
