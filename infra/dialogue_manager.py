import pandas as pd

"""
class DialogueManager(Component):

    def __init__(self, tracker, agent):
        super().__init__()
        self.tracker = tracker
        self.agent = agent
        self.tracker.connect(agent)
"""


def excel_to_df(file_path):
    return pd.read_excel(file_path, 0)


def read_sorted_solution(df, part, error):
    df = df.loc[(df['Parts'] == part) & (df['Error'] == error)]
    df = df.sort_values('appear_time')
    print(df)
    solutions = df.Solution.tolist()
    return solutions[::-1]


def get_solutions(part, error, filename):
    """
    Look for possible solutions from database
    :return:
        A list of solutions based on given part and error from most frequent to least frequent.
    """

    df = excel_to_df(filename)
    return read_sorted_solution(df, part, error)


filename = '../doc/cnc_troubleshooting.xlsx'
part = 'Tool magazine(Umbrella type)'
error = 'Noise for tool changing'