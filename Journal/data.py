import requests
from DATA.data import Journal
url = Journal.url
journal = Journal.journal

session = requests.Session()
session.get(url)

csrfmiddlewaretoken=session.cookies['csrftoken']

objects = {}

token = Journal.token

user = {"username": "",
        "password": ""}

temp = {}

temp_calls = {}