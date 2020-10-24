from infra.chatbot import Chatbot
from inter.cli_interface import CLI_Interface
from nlu.dumb_nlu import Dumb_NLU

if __name__ == '__main__':
    interface = CLI_Interface()
    nlu = Dumb_NLU()
    nlu_test_bot = Chatbot([interface, nlu])
    nlu_test_bot.step()

