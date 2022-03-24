from flask import Flask, render_template
from flask import request
from todo_app.flask_config import Config
from todo_app.data.trello_items import trello_get_items
from todo_app.data.trello_items import trello_add_item
from todo_app.data.trello_items import trello_complete_item
from todo_app.data.trello_items import trello_todo_item
from datetime import datetime
import requests
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')
    def index():
        item_view_model = ViewModel(items = trello_get_items(), result_message=None)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        if not request.form['title'].isspace():
            result_message = trello_add_item(request.form['title'], request.form['desc'], request.form['datepicker'])
        else:
            result_message = "No title given"
        item_view_model = ViewModel(trello_get_items(), result_message)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/complete', methods=['GET'])
    def complete():
        if not request.args.get('id','').isspace():
            result_message = trello_complete_item(request.args.get('id',''))
        else:
            result_message = "didnt get an item id"
        item_view_model = ViewModel(trello_get_items(), result_message)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/reset', methods=['GET'])
    def reset():
        if not request.args.get('id','').isspace():
            result_message = trello_todo_item(request.args.get('id',''))
        else:
            result_message = "didnt get an item id"
        item_view_model = ViewModel(trello_get_items(), result_message)
        return render_template('index.html', view_model=item_view_model)

    return app
class ViewModel:
    def __init__(self, items, result_message):
        self._items = items
        self._result_message = result_message
    @property
    def items(self):
        return self._items
    def result_message(self):
        return self._result_message
    def todo_items(self):
        return filter_items_by_status(self._items, "To Do")
    def doing_items(self):
        return filter_items_by_status(self._items, "Doing")
    def done_items(self):
        return filter_items_by_status(self._items, "Done")

def filter_items_by_status(items, status):
        filtered_items=[]
        for item in items:
            if item.status == status:
                filtered_items.append(item)
        return filtered_items