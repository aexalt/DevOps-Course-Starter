from flask import Flask, render_template
from flask import request, redirect
from flask_login import LoginManager
from flask_login import login_required
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
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()
    @login_manager.unauthorized_handler
    def unauthenticated():
        url = f"https://github.com/login/oauth/authorize?client_id={os.getenv('CLIENT_ID')}"
        return redirect(url)
        pass # Add logic to redirect to the GitHub OAuth flow when unauthenticated
    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
    login_manager.init_app(app)

    @app.route('/login/callback')
    def callback():
        params = {
            "code": request.args['code'],
            "client_id": os.getenv('CLIENT_ID'),
            "client_secret": os.getenv('CLIENT_SECRET')
        }
        headers = {"Accept": "application/json"}
        response = requests.post("https://github.com/login/oauth/access_token", params = params, headers = headers)

        auth_header= {"Authorization": f"Bearer {response.json()['access_token']}"}

        api_response = requests.get("https://api.github.com/user", headers = auth_header)


    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(items = trello_get_items(), result_message=None)
        return render_template('index.html', view_model=item_view_model)

    
    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        if not request.form['title'].isspace():
            result_message = trello_add_item(request.form['title'], request.form['desc'], request.form['datepicker'])
        else:
            result_message = "No title given"
        item_view_model = ViewModel(trello_get_items(), result_message)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/complete', methods=['GET'])
    @login_required
    def complete():
        if request.args.get('id'):
            result_message = trello_complete_item(request.args.get('id',''))
        else:
            result_message = "didnt get an item id"
        item_view_model = ViewModel(trello_get_items(), result_message)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/reset', methods=['GET'])
    @login_required
    def reset():
        if request.args.get('id'):
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