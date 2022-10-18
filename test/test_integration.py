import pytest
from todo_app.data import trello_items
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import mongomock

@pytest.fixture
def client():
 file_path = find_dotenv('.env.test')
 load_dotenv(file_path, override=True)
 
 with mongomock.patch(servers=(('fakemongo.com', 27017),)):
    test_app = app.create_app()
    with test_app.test.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(trello_items, 'call_trello_api', get_lists_stub)
    response = client.pymongo.MongoClient()
    assert response.acknowledged
    assert 'Test card' in response.data.decode()


def test_complete(monkeypatch, client):
    monkeypatch.setattr(trello_items, 'call_trello_api', get_lists_stub)
    response = client.get('/complete?id=123abc')
    assert response.status_code == 200
    assert 'successful' in response.data.decode()

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.status_code = 200
    def json(self):
        return self.fake_response_data

def get_lists_stub(uri_path,httpMethod,add_querys):
    fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card', 'desc': 'test desc', 'due' : None}],
     }]
    return StubResponse(fake_response_data)