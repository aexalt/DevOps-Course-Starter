from flask import session
from datetime import datetime
import requests
import os
import pymongo

def trello_get_items():
    items=[]
    uri_path = "" 
    querys = {
        "cards": "open"
    }
    response = call_trello_api(uri_path, "GET", querys)

    for trello_list in response:
        items.append(Item.from_trello_card(trello_list))
    return items

def trello_add_item(title, desc, date):

    uri_path = ""

    querys = {
        "name": title,
        "desc": desc,
        "due": date,
        "status": "To Do"
    }

    response = call_trello_api(uri_path, "POST", querys)

    return http_status_text(response)

def trello_complete_item(id):

    uri_path = id

    querys = {
        "status": "Done"
    }

    response = call_trello_api(uri_path, "PUT", querys)

    return http_status_text(response)

def trello_todo_item(id):

    uri_path = id

    querys = {
         "status": "To Do",
    }

    response = call_trello_api(uri_path, "PUT", querys)

    return http_status_text(response)


def call_trello_api(id,httpMethod,add_querys):

    #url = "https://api.trello.com" + uri_path
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db["listcollection"]

    if(httpMethod == "POST"):
        result = collection.insert_one(add_querys)
    elif(httpMethod == "PUT"):
        result = collection.update_one({'_id':id}, { "$set": add_querys })
    else:
        result = collection.find()

    return result


def  http_status_text(response):
    if(response.acknowledged):
        return "successful"
    else:
        return "failed"

class Item: 
    def __init__(self, id, name, desc, due, status = 'To Do'): 
        self.id = id 
        self.name = name 
        self.desc = desc
        self.due = due
        self.status = status 
        
    
    @classmethod 
    def from_trello_card(cls, card): 
        return cls(card['_id'], card['name'], card['desc'], card['due'], card['status']) 

def datetime_format_old(value, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    if value is not None:
        return datetime.strptime(value,format)
    else:
        return None

def datetime_format(value, format='%m/%d/%Y'):
    if value is not None:
        return datetime.strptime(value,format)
    else:
        return None