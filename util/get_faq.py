import pandas as pd


def get_faq(FILENAME):

    df = pd.read_excel(FILENAME)

    errors = {}


    for index, row in df.iterrows():
        row = row.to_list()
        if row[14] in errors:
            errors[row[14]] += row[-1]
        else:
            errors[row[14]] = 0

    res = [i for i in errors.keys() if errors[i] > 0]
    res.sort(key=lambda x:errors[x], reverse=True)

    return res
