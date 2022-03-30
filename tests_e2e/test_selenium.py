import os
from threading import Thread
from todo_app import app
from selenium.webdriver import Edge
driver = Edge()

load_dotenv('.env')

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield drive

def create_trello_board():
    uri_path = "/1/boards"

    querys = {
        "name": "e2e test board"
    }
    response = call_trello_api(uri_path, "POST", querys)
    return response

def delete_trello_board(board_id):
    uri_path = "/1/boards/" + board_id

    response = call_trello_api(uri_path, "DELETE", None)
    return response