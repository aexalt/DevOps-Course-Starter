from flask import Flask, render_template
from flask import request
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
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