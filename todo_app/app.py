from flask import Flask, render_template
from flask import request
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item
from todo_app.data.session_items import get_item
from todo_app.data.session_items import save_item
from todo_app.data.trello_items import trello_get_items
from todo_app.data.trello_items import trello_add_item
from todo_app.data.trello_items import trello_complete_item
from todo_app.data.trello_items import trello_todo_item

import requests
import os

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    return render_template('index.html', result = trello_get_items())

@app.route('/add', methods=['POST'])
def add():
    if not request.form['title'].isspace():
        add_result = trello_add_item(request.form['title'], request.form['desc'])
        return render_template('index.html', success=add_result, result = trello_get_items())
    else:
        return render_template('index.html', success="No title given", result = trello_get_items())

@app.route('/complete', methods=['GET'])
def complete():
    error = None
    if not request.args.get('id','').isspace():
        complete_result = trello_complete_item(request.args.get('id',''))
        return render_template('index.html', success=complete_result, result = trello_get_items())
    else:
        return render_template('index.html', success="didnt get an item id", result = get_items())

@app.route('/reset', methods=['GET'])
def reset():
    error = None
    if not request.args.get('id','').isspace():
        reset_result = trello_todo_item(request.args.get('id',''))
        return render_template('index.html', success=reset_result, result = trello_get_items())
    else:
        return render_template('index.html', success="didnt get an item id", result = get_items())