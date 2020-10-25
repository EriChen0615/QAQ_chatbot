from flask import Flask, render_template, request, json, jsonify
import pandas as pd
import dialogue_manager as dialogue_manager
import NB_nlu as NB_nlu


def get_faq(FILENAME):
    '''
    This function get the FAQ list from the cnc_troubleshooting.xlsx file.
    and return the list of errors in descending order of frequencies.
    :param FILENAME: string
    :return: re -> list
    '''
    df = pd.read_excel(FILENAME)

    errors = {}

    for index, row in df.iterrows():
        row = row.to_list()
        if row[1] in errors:
            errors[row[1]] += row[-1]
        else:
            errors[row[1]] = 0

    res = [i for i in errors.keys() if errors[i] > 0]
    res.sort(key=lambda x: errors[x], reverse=True)

    return res


app = Flask(__name__)


# main-page
@app.route('/')
def index():
    return render_template("index.html")


# page with FAQ sidebar
@app.route('/side')
def home():
    return render_template("side.html")


# initiate NLU operators
nlu = NB_nlu.NB_NLU()
dl = dialogue_manager.DialogueManager()
FILENAME = "data/cnc_troubleshooting.xlsx"


# Handle AJAX request and interaction with javascript
@app.route('/sendDate', methods=['GET', 'POST'])
def form_data():
    msg = json.loads(list(request.form.lists())[0][0])
    # Get the message sent by user
    txt = msg['query']
    msg = dialogue_manager.mergeprocess(nlu, dl, txt)
    faq_list = get_faq(FILENAME)
    return jsonify({'msg': msg, 'faq': faq_list})


if __name__ == '__main__':
    app.run()
