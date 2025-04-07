import json
import os
from db import save_all_data, load_all_data
users = {}


def id_exist(id_):
    if id_ not in users.keys():
        users[id_] = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Відповідай коротко як у месенджерах , речення починай з маленької букви , ти - спокійний , майже беземоційний хлопець , Богдан , ти трохи знаєшся на програмуванні"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "ок, зрозумів"
                    }
                ]
            }
        ]

def add_user_message(id_, text):
    id_exist(id_)
    users[id_].append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": text
            }
        ]
    })
    save_all_data(users)

def add_system_message(id_, text):
    id_exist(id_)
    users[id_].append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": text
            }
        ]
    })
    save_all_data(users)

def get_mess(id_):
    id_exist(id_)
    return users[id_]

