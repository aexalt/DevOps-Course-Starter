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
            session["todo_list_id"] = trello_list['id']
        elif trello_list['name'] == 'Done':
            session["done_list_id"] = trello_list['id']
        for card in trello_list['cards']:
            Items.append(Item.from_trello_card(card, trello_list))
    return Items

def trello_add_item(title, desc):

    uri_path = "/1/cards"

    querys = {
        "idList": session.get("todo_list_id"),
        "name": title,
        "desc": desc
    }

    response = call_trello_api(uri_path, "POST", querys)

    return http_status_text(response)

def trello_complete_item(id):

    uri_path = "/1/cards/" + id

    querys = {
        "idList": session.get("done_list_id")
    }

    response = call_trello_api(uri_path, "PUT", querys)

    return http_status_text(response)

def trello_todo_item(id):

    uri_path = "/1/cards/" + id

    querys = {
        "idList": session.get("todo_list_id"),
    }

    response = call_trello_api(uri_path, "PUT", querys)

    return http_status_text(response)


def call_trello_api(uri_path,httpMethod,add_querys):

    url = "https://api.trello.com" + uri_path
    querys = {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_API_TOKEN")
    }
    querys.update(add_querys)
    return requests.request(httpMethod, url, params=querys)


def  http_status_text(response):
    if(response.status_code) == 200:
        return "success"
    else:
        return "failed"

class Item: 
    def __init__(self, id, name, desc, status = 'To Do'): 
        self.id = id 
        self.name = name 
        self.desc = desc 
        self.status = status 
    
    @classmethod 
    def from_trello_card(cls, card, list): 
        return cls(card['id'], card['name'], card['desc'], list['name']) 

