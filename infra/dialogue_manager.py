from .component import Component
import pandas as pd
import numpy as np

class DialogueManager(Component):

    def __init__(self,):# imput):
        super().__init__()
        # self.tracker = tracker
        # self.agent = agent
        # self.tracker.connect(agent)
        """
        input type:

        ["parts"], ["trouble"], ["states"]

        ["state=greeting, abort, thanks, problem, yes, no"]
        """
        #self.input = imput
        self.setup1()
        self.last_state = None
        # self.learnparameter=1
        self.state_counter = 0
        self.filename = '..doc/cnc_troubleshooting.xlsx'
        self.df = self.excel_to_df()
        self.df_stats = self.get_solutions(self.part, self.trouble)

    def setup(self):
        pass

    def setup1(self):
        # print("Dialogue Manager is setup!")
        self.part = self.input["parts"]
        # self.part_tracker=[]
        self.trouble = self.input["trouble"]
        self.state = self.input["states"]
        pass

    def input_debug(self, intm):
        self.input = intm
        self.setup1()

    def do_step(self):
        # self.tracker.input = self.input
        # self.tracker.run()
        # self.agent.run()
        if self.state == "greeting":
            response_msg = self.greeting()
        elif self.state == "thanks":
            #print(1111)
            response_msg = self.thanks()

        elif self.state == "trouble" or "yes" or "no":
            response_msg = self.trouble_shooting()
        self.output = response_msg
        #print(response_msg, self.state_counter, self.state)
        self.last_state = self.state

    def to_front(self, action):
        return {'response': action['response'], 'browser_action': 'reply'}

    def greeting(self):
        return "Hello, how can I help you?"

    def thanks(self):
        #print(self.part, self.trouble, self.state_counter)
        i = 0
        while self.df.loc[i, 'Parts'] != self.part or self.df.loc[i, 'Error'] != self.trouble or self.df.loc[
            i, 'Solution'] != self.df_stats[self.state_counter - 1]:
            i += 1
        self.df.loc[i, 'appear_time'] += 1
        self.df.to_excel(self.filename, sheet_name='Sheet1', index=False, header=True)

        self.df.to_excel(self.filename)
        #self.__init__()
        return "My pleasure"

    def trouble_shooting(self):
        """
        Intellegent: if one field is empty but only one candidate, can autofill
        gives suggestions based on historical features
        feature to be added: 1. suggestions refer to online forum
        feature to be tested:1. add customized measurements
        """

        if self.part is None or self.trouble is None:
            return "I'm sorry, I couldn't understand. Good luck :-D"
        elif self.part is None:
            candidates=self.df.loc[(self.df['Error'] == self.trouble)]
            candidates=candidates.Parts.tolist()
            if len(candidates)==1:
                self.part=candidates[0]
                self.do_step()
                return 0
            else:
                return "Which part has problem? Is it"+','.join(candidates)+"?"
        elif self.trouble is None:
            candidates = self.df.loc[(self.df['Parts'] == self.part)]
            candidates = candidates.Errors.tolist()
            if len(candidates) == 1:
                self.trouble = candidates[0]
                self.do_step()
                return 0
            else:
                return "What's the problem with"+self.part+"?Is it"+','.join(candidates)+"?"
        else:
            self.state_counter = self.state_counter + 1
            return self.df_stats[self.state_counter - 1]

    def excel_to_df(self):
        return pd.read_excel(self.filename, 0)

    def read_sorted_solution(self, df, part, error):
        df = df.loc[(df['Parts'] == part) & (df['Error'] == error)]
        df = df.sort_values('appear_time')
        # print(df)
        solutions = df.Solution.tolist()
        return solutions[::-1]

    def get_solutions(self, part, error):
        """
        Look for possible solutions from database
        :return:
            A list of solutions based on given part and error from most frequent to least frequent.
        """
        return self.read_sorted_solution(self.df, part, error)

    def study(self, part, trouble, new_solution):
        """
        Add a new solution from user feedback if all the possible solutions are declined.
        """
        df = pd.read_excel(self.filename, 0)
        i = 0
        while self.df.loc[i, 'Parts'] != self.part or self.df.loc[i, 'Error'] != self.trouble or self.df.loc[
            i, 'Solution'] != self.df_stats[self.state_counter - 1]:
            i += 1

        pd.DataFrame(np.insert(df.values, i + 1, values=[part, trouble, new_solution, 0], axis=0))

        df.to_excel(self.filename)

if __name__ == '__main__':
    input = {"parts": "Tool magazine(Umbrella type)", "trouble": "Noise for tool changing", "states": "trouble"}
    m = DialogueManager(imput=input)

    m.run()
    input = {"parts": "Tool magazine(Umbrella type)", "trouble": "Noise for tool changing", "states": "trouble"}
    m.input_debug(input)
    m.run()
    input = {"parts": "Tool magazine(Umbrella type)", "trouble": "Noise for tool changing", "states": "thanks"}
    m.input_debug(input)
    m.run()
