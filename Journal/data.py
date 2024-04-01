import requests

url = "https://journalelectro.pythonanywhere.com/login/"
journal = "https://journalelectro.pythonanywhere.com/journal/student-1328"

session = requests.Session()
session.get(url)

csrfmiddlewaretoken=session.cookies['csrftoken']

objects = {}

token = '6159454834:AAGtkISBzGFE8rBtD4Ksqy1YeBKRpqpSOL8'

user = {"username": "",
        "password": ""}

temp = {}

temp_calls = {}