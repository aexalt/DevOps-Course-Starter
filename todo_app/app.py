from flask import Flask, render_template
from flask import request
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item
from todo_app.data.session_items import get_item
from todo_app.data.session_items import save_item

import requests
import os

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    url = ""

    os.getenv("TRELLO_API_KEY")

    querys = {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_API_TOKEN"),
        "cards": "open"
    }

    response = requests.request("GET", url, params=querys).json()
    #respons_json = response.json()

    for tello_list in response_json:
        for card in trello_list['cards']:
            print(card)
            card['status'] = trello_list['name']

    items = response_json[0]['cards']

    return render_template('index.html', result = get_items())

@app.route('/add', methods=['POST'])
def add():
    error = None
    if request.method == 'POST':
        if not request.form['title'].isspace():
            add_item(request.form['title'])
            return render_template('index.html', success="successfully written", result = get_items())
        else:
            error = 'no title'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', success="error ", result = get_items())

@app.route('/complete', methods=['GET'])
def complete():
    error = None
    if not request.args.get('id','').isspace():
        item = get_item(request.args.get('id',''))
        item['status'] = 'complete'
        save_item(item)
        return render_template('index.html', success="successfully written", result = get_items())
    else:
        return render_template('index.html', success="didnt get an item id", result = get_items())