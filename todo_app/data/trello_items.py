from flask import session
import requests
import os

def trello_get_items():
    Items=[]
    uri_path = "/1/boards/" + os.getenv("TRELLO_BOARD_ID") +"/lists"
    querys = {
        "cards": "open"
    }
    response = call_trello_api(uri_path, "GET", querys)

    for trello_list in response:
        for card in trello_list['cards']:
            Items.append(Item.from_trello_card(card, trello_list))
    return session.get('items', Items)

def trello_add_item(title):
    items = trello_get_items()
    print(items)
    uri_path = "/1/cards"
    # Determine the ID for the item based on that of the previously added item
    #id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    #items.append(item)
    #session['items'] = items

    return item

def call_trello_api(uri_path,httpMethod,add_querys):

    url = "https://api.trello.com" + uri_path
    querys = {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_API_TOKEN"),
    }
    querys.update(add_querys)
    print(httpMethod, url, querys)
    return requests.request(httpMethod, url, params=querys).json()

class Item: 
    def __init__(self, id, name, status = 'To Do'): 
        self.id = id 
        self.name = name 
        self.status = status 
    
    @classmethod 
    def from_trello_card(cls, card, list): 
        return cls(card['id'], card['name'], list['name']) 

