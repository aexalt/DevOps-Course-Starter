from flask import session
import requests
import os

def trello_get_items():
    Items=[]
    uri_path = "/1/boards/" + os.getenv("TRELLO_BOARD_ID") +"/lists"
    querys = {
        "cards": "open"
    }
    response = call_trello_api(uri_path, "GET", querys).json()

    for trello_list in response:
        if trello_list['name'] == 'To Do':
            session["list_id"] = trello_list['id']
        for card in trello_list['cards']:
            Items.append(Item.from_trello_card(card, trello_list))
    print(Items)
    return Items

def trello_add_item(title):

    uri_path = "/1/cards"

    querys = {
        "idList": session.get("list_id")
    }

    response = call_trello_api(uri_path, "POST", querys)

    if(response.status_code) == 200:
        result = "success"
    else:
        result = "failed to add"

    return result

def call_trello_api(uri_path,httpMethod,add_querys):

    url = "https://api.trello.com" + uri_path
    querys = {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_API_TOKEN"),
    }
    querys.update(add_querys)
    return requests.request(httpMethod, url, params=querys)

class Item: 
    def __init__(self, id, name, status = 'To Do'): 
        self.id = id 
        self.name = name 
        self.status = status 
    
    @classmethod 
    def from_trello_card(cls, card, list): 
        return cls(card['id'], card['name'], list['name']) 

