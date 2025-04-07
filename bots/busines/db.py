import sqlite3
import json
from threading import Lock

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
lock = Lock()

# створюємо таблицю якщо вона не існує
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    data TEXT
)
''')
conn.commit()

# Функція для збереження даних
def save_data(id_, data):
    try:
        json_data = json.dumps(data)
        with lock:
            cursor.execute('INSERT OR REPLACE INTO users (id, data) VALUES (?, ?)', (id_, json_data))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving data: {e}")

# Зберігаємо всі дані з словника в базу даних
def save_all_data(users):
    for id_, jsn in users.items():
        save_data(id_, jsn)

def close_database():
    cursor.close()
    conn.close()

def load_all_data(users):
    try:
        with lock:
            cursor.execute('SELECT id, data FROM users')
            rows = cursor.fetchall()
            data_dict = {}
            for id_, data in rows:
                data_dict[id_] = json.loads(data)
            users.update(data_dict)
    except sqlite3.Error as e:
        print(f"Error loading data: {e}")