from dumb_nlu import Dumb_NLU
from component import Component
import pandas as pd
import numpy as np

"""
Intellegent: if one field is empty but only one candidate, can autofill
gives suggestions based on historical features
feature to be added: 1. suggestions refer to online forum
                     2. add top search list
                     3. maintaince
feature to be tested:1. add customized measurements

"""


class DialogueManager(Component):

    def __init__(self):
        """
        create a Dialogue Manager object
        :param
        :attributes
        input: get input from nlu
                input is a dictionary with three attributes: parts, error, states
                states[None=detect parts/error, yes/no=feedback from the user for the validity of the solution]
        setup1: transfer input to inner attributes(see function)
        last_state, state: None(to identify the problem), yes(we're done!), or no(the pass the next solution)
        state_counter: count how many states has been provided but failed
        filename: fixed variable for file path
        df: dataframe to the data file
        df_stats: a list of solutions, ranked based on success frequency

        :return None
        """
        super().__init__()
        # self.tracker = tracker
        # self.agent = agent
        # self.tracker.connect(agent)

        self.input = None
        # self.setup1()
        self.last_state = None
        self.state = None
        # self.learnparameter=1
        self.state_counter = 0
        self.filename = 'data/cnc_troubleshooting.xlsx'
        self.df = self.excel_to_df()
        self.df_stats = []
        self.msg = ""
        self.new_solution = ""


    def setup(self):
        pass

    def setup1(self):
        """
        deal with input and update existing variables.
        if input contains an previously unknown attribute, then update the attribute
        else, create a placeholder/leave nothing
        DO NOT PERFORM COLLISION DETECTION: will keep the newest valid solution
        :return: None
        """
        # print("Dialogue Manager is setup!")
        if "parts" in self.input and self.input['parts']:
            self.part = self.input["parts"]
        if "error" in self.input and self.input['error']:
            self.error = self.input["error"]
        self.last_state = self.state
        if "solution" in self.input:
            self.new_solution = self.input["solution"]
        # print(self.input)
        self.state = self.input["state"]
        try:
            self.part
        except AttributeError:
            self.part = None
        try:
            self.error
        except AttributeError:
            self.error = None

    def input_debug(self, intm):
        """
        for debug and using the object as a function
        e.g. object.input_debug(<input dictionary>)
             get_result=object.do_step()
        :param intm: input
        :return: none
        """
        self.input = intm
        self.setup1()
        return 0

    def do_step(self):
        # self.tracker.input = self.input
        # self.tracker.run()
        # self.agent.run()
        # if self.state == "greeting":
        #    response_msg = self.greeting()
        # elif self.state == "thanks":
        #    response_msg = self.thanks()
        """
        the main control of the program
        If either part is missing, request user to describe the problem using trouble_shooting
        If both parts are presented, provide the solution by solution_provider()
            (if problem solved, it will jump to thanks() as indicated in the solution_provider())
        Additionally, if it is "yes", case closed and object inits itself.
        :return: response_msg to the UI
        """
        if ((not self.part or not self.error) and self.state == 'no') or not self.state:
            response_msg = self.trouble_shooting()
        else:
            response_msg = self.solution_provider()
        self.output = response_msg
        print(response_msg)  # , self.state_counter, self.state)
        self.msg = response_msg
        self.last_state = self.state
        if self.state == "yes":
            pass  # self.__init__()
        return response_msg

    def to_front(self, action):
        """
        aborted!
        """
        return {'response': action['response'], 'browser_action': 'reply'}

    def greeting(self):
        """
        Aborted! Replaced by greeting in UI
        :return:
        """
        return "Hello, how can I help you?"

    def thanks(self):
        """
        Run this function when the user solved the problem
        Update the methods on a sheet
        :return: Answer politely with a speck of pride. Our chatbot is well-educated gentleman/lady
        """
        # print(self.part, self.error, self.state_counter)
        i = 1
        while self.df.loc[i, 'Parts'] != self.part or self.df.loc[i, 'Error'] != self.error or self.df.loc[
            i, 'Solution'] != self.df_stats[self.state_counter - 2]:
            i += 1
        self.df.loc[i, 'appear_time'] += 1
        self.df.to_excel(self.filename, sheet_name='Sheet1', index=False, header=True)

        self.df.to_excel(self.filename, index=False)
        # self.__init__()
        return "My pleasure."

    def trouble_shooting(self):
        """
        Try to find some information form our poor dumb master. Hopefully he/she will say something reasonable
        :return: if none of "parts" and "error" is understood, give it another try (or am I)?
                if one part is missing: list all I know that fits another parameter. That's the best I can do.
                hope there is something for my poor master
        """
        """
        Intellegent: if one field is empty but only one candidate, can autofill
        gives suggestions based on historical features
        feature to be added: 1. suggestions refer to online forum
        feature to be tested:1. add customized measurements
        """
        if not self.state:
            return "I'm sorry, TROUBLE!!"
        elif self.state == 'greeting':
            return "Please tell me more about your issue!"
        elif not self.part and not self.error:
            return "I'm sorry, I couldn't understand. Good luck :-D"
        elif not self.part:
            candidates = self.df.loc[(self.df['Error'] == self.error)]
            candidates = candidates.Parts.tolist()
            candidates = list(set(candidates))
            if len(candidates) == 1:
                self.part = candidates[0]
                self.do_step()
                return 0
            else:
                return "Which part has this problem? Is it " + ','.join(candidates) + "?"
        elif not self.error:
            self.df = self.excel_to_df()
            candidates = self.df.loc[(self.df['Parts'] == self.part)]
            candidates = candidates.Error.tolist()
            candidates = list(set(candidates))
            if len(candidates) == 1:
                self.error = candidates[0]
                self.do_step()
                return 0
            else:
                return "What's the problem with " + self.part + "? Is " + ', '.join(candidates).lower() + "?"
        else:
            return

    def solution_provider(self):
        """
        Solution time!
        Trace how many solutions I have provided and provide the next possible solution based on the knowledge.
        If there's no more I can provide, sorry!
        If my master solved the problem, hooray! Jump to the wrap up thanks()
        :return: solution!
        """
        if self.state == "no":
            if self.part and self.error:
                self.df_stats = self.get_solutions(self.part, self.error)
            self.state_counter = self.state_counter + 1
            # print(self.error, self.part, self.state_counter, self.df_stats)
            if self.state_counter > len(self.df_stats):
                # self.__init__()
                return "Sorry, it is beyond my scope. Please tell me how you solve this problem if possible, " \
                       "so that I can help next time! $Enter your solution with the dollar signs$"  # provide
                # user-defined manual
            return "Try to " + self.df_stats[self.state_counter - 1].lower() + ". Does it work?"
        elif self.state == "solution":
            self.study()
            return "Thank you for your information!"
        elif self.state == "yes":
            print(self.df_stats)
            print(self.state_counter)
            return self.thanks()
        elif self.state == 'greeting':
            return "Please tell me more about your issue!"

    def excel_to_df(self):
        """
        as indicated
        :return:
        """
        return pd.read_excel(self.filename, 0)

    def read_sorted_solution(self, df, part, error):
        """read file"""
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

    def study(self):
        """
        Add a new solution from user feedback if all the possible solutions are declined.
        """
        df = pd.read_excel(self.filename, 0)
        df2 = pd.DataFrame([self.part,self.error,self.new_solution,0])
        df = df.append(df2, ignore_index=True)

        df.to_excel(self.filename, index=False)


def mergeprocess(nlu, m, text):
    input = nlu.process(text)
    print(input)
    m.input_debug(input)
    m.run()
    console_msg = m.msg
    if console_msg == "Sorry, it is beyond my scope." or console_msg == "My pleasure.":
        m.__init__()
    return console_msg


def mergeprocess_fake(nlu, m, text):
    input = {"parts": "Tool magazine (Umbrella type)", "error": "Tool number in chaos", "state": 'study'}
    m.input_debug(input)
    m.run()
    console_msg = m.msg
    if console_msg == "Sorry, it is beyond my scope." or console_msg == "My pleasure.":
        m.__init__()
    return console_msg


if __name__ == '__main__':
    """
    input is a dictionary with three attributes: parts, error, states
    states[None=detect parts/error, yes/no=feedback from the user for the validity of the solution]
    """
    m = DialogueManager()
    """test for local file"""
    """input = {"parts": None, "error": "Noise for tool changing umbrella", "state": "no"}

    m.input_debug(input)
    m.run()"""
    input = {"parts": None, "error": None, "state": 'greeting'}
    m.input_debug(input)
    m.run()
    """
    input = {"parts": "Tool magazine(Umbrella type)", "error": "Noise for tool changing", "state": "no"}
    m = DialogueManager()
    m.input_debug(input)
    m.run()"""

    """testing for MERGING"""
    """
    natural_language = Dumb_NLU()
    m = DialogueManager()
    user_input = 'hi'
    mergeprocess(natural_language, m, user_input)
    
    user_input = 'The change 4 noise milling is not working.,,,'
    mergeprocess(natural_language, m, user_input)
    user_input = 'yes'
    mergeprocess(natural_language, m, user_input)
    """

"""
flow chart
0. initialize
1. input.debug()
2. run():
    if attributes not complete: ask   trouble_shooting()
    if attributes complete:  solution_provider()->previous solution not correct, have another method, 
                                                  go through the list and suggest(use state_counter, get_solutions())
                                                ->previous solutionnot correct no more method,
                                                  sorry, and initialise
                                                ->previous solution correct
                                                  go to thanks(), and initialize
3. waiting for input.
"""
