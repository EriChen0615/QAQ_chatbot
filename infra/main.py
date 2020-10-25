from flask import Flask, render_template, request, json, jsonify
import pandas as pd
import infra.dialogue_manager as dialogue_manager
import infra.dumb_nlu as dumb_nlu


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
    res.sort(key=lambda x: errors[x], reverse=True)

    return res


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dev')
def dev():
    return render_template("dev.html")


@app.route('/side')
def home():
    return render_template("side.html")


nlu = dumb_nlu.Dumb_NLU()
dl = dialogue_manager.DialogueManager()


@app.route('/sendDate', methods=['GET', 'POST'])
def form_data():
    msg = json.loads(list(request.form.lists())[0][0])
    txt = msg['query']
    FILENAME = "static/dataset/cnc_troubleshooting.xlsx"
    faq_list = get_faq(FILENAME)

    return jsonify({'status': '0', 'msg': dialogue_manager.mergeprocess(nlu, dl, txt), 'faq': faq_list})


if __name__ == '__main__':
    app.run()
