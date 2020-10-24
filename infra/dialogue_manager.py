from .component import Component
from .tracker import Tracker
from .agent import Agent
import pandas as pd

class DialogueManager(Component):

    def __init__(self, tracker, agent):
        super().__init__()
        # self.tracker = tracker
        # self.agent = agent
        # self.tracker.connect(agent)
        """
        input type:

        ["parts"], ["trouble"], ["state"]

        ["state=greeting, abort, thanks, problem, yes, no"]
        """
        self.part = self.input["parts"]
        # self.part_tracker=[]
        self.trouble = self.input["trouble"]
        self.state = self.input["states"]
        self.last_state = None
        # self.learnparameter=1
        self.stats_counter = 0
        self.filepath = '../doc/cnc_troubleshooting.xlsx'
        self.df = excel_to_df(filename)

    def setup(self):
        print("Dialogue Manager is setup!")

    def do_step(self):
        # self.tracker.input = self.input
        # self.tracker.run()
        # self.agent.run()
        if self.state == "greeting":
            response_msg = self.greeting()
        elif self.state == "thanks":
            response_msg = self.thanks()
        elif self.state == "trouble" or "yes" or "no":
            response_msg = self.trouble_shooting(self.part, self.trouble)
        self.output = response_msg
        self.last_state = self_state

    def to_front(self, action):
        return {'response': action['response'], 'browser_action': 'reply'}

    def greeting():
        return "Hello, how can I help you?"

    def thanks(self):
        self.df[self.df_stats[self.state_counter]]["appear_time"] = df[self.df_stats[self.state_counter]]["appear_time"] + 1
        df
        # self.init()
        return "My pleasure"

    def trouble_shooting(self, part, trouble):
        """
        if part==None:
            for candidate in df_manual:
                if candidate not in self.part:
                    self.part.append(candidate)
                    return "I'm sorry. Do you mean there is a problem in"+candidate+"?"
                    break
                return "I'm sorry, I don't know other parts"
            #return "Is it one of the following:"+.join{df.["parts"]}
        if part!=None and trouble==None:
        """
        df_stats=self.get_solution(part, trouble)
        if part == None or trouble == None:
            return "I'm sorry, I couldn't understand. Good luck :-D"
        self.state_counter = self.statecounter + 1
        df_stats=get_solution(part, trouble)
        return df_stats([self.state_counter - 1])


    def excel_to_df(self):
        return pd.read_excel(self.file_path, 0)

    def read_sorted_solution(self, df, part, error):
        df = df.loc[(df['Parts'] == part) & (df['Error'] == error)]
        df = df.sort_values('appear_time')
        #print(df)
        solutions = df.Solution.tolist()
        return solutions[::-1]

    def get_solutions(self,part, error):
        """
        Look for possible solutions from database
        :return:
            A list of solutions based on given part and error from most frequent to least frequent.
        """
        return read_sorted_solution(self.df, part, error)

if __name__=='__main__':
    filename = '../doc/cnc_troubleshooting.xlsx'
    part = 'Tool magazine(Umbrella type)'
    error = 'Noise for tool changing'
