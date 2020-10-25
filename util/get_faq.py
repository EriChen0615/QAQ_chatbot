import pandas as pd


def get_faq(FILENAME):

    df = pd.read_excel(FILENAME)

    errors = {}


    for index, row in df.iterrows():
        row = row.to_list()
        if row[1] in errors:
            errors[row[1]] += row[-1]
        else:
            errors[row[1]] = 0

    res = [i for i in errors.keys() if errors[i] > 0]
    res.sort(key=lambda x:errors[x], reverse=True)

    return res
