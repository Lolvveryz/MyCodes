import telebot
from telebot import types
import sqlite3
import datetime
import mock

# Використання змінної з моковими даними 
bot = telebot.TeleBot(mock.tbot)

# Створення бази даних і таблиці
def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat INTEGER NOT NULL,
                username TEXT NOT NULL,
                birthdate TIMESTAMP NOT NULL
            )
        ''')
        conn.commit()

init_db()

# Функція для роботи з БД (автоматичне відкриття/закриття)
def db_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if commit:
            conn.commit()
        
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()

@bot.message_handler(commands=["start"])
def start(mess):
    bot.send_message(mess.chat.id, "Вітаю в боті рахування часу з дня народження!\n\nВведіть вашу дату народження у форматі \nдд.мм.рррр")

@bot.message_handler(content_types=["text"])
def main(mess):
    # Перевіряємо, чи користувач вже є в БД
    fetched_data = db_query("SELECT id FROM Users WHERE chat = ?", (mess.chat.id,), fetchone=True)

    if fetched_data is None:
        # Якщо користувача немає у БД, пробуємо зберегти його дату народження
        try:
            date_parts = list(map(int, mess.text.split(".")))
            birth_date = datetime.datetime(date_parts[2], date_parts[1], date_parts[0])

            # Додаємо запис у базу
            db_query("INSERT INTO Users (chat, username, birthdate) VALUES (?, ?, ?)", 
                     (mess.chat.id, mess.from_user.username, birth_date), commit=True)


            markup = types.ReplyKeyboardMarkup(row_width=1)
            week_button = types.KeyboardButton("Cкільки тижнів пройшло")
            day_button = types.KeyboardButton("Cкільки днів пройшло")
            change_button = types.KeyboardButton("Змінити дату народження")
            markup.add(day_button, week_button, change_button)
            bot.send_message(mess.chat.id, "Я зберіг ваші дані, можете рахувати дні з вашого народження!", reply_markup=markup)

        except Exception as ex:
            bot.send_message(mess.chat.id, f"Схоже, що щось не так. Перевірте формат дати та спробуйте ще раз.\nПомилка: {ex}")

    else:
        # Якщо користувач вже є в БД
        if mess.text == "Cкільки тижнів пройшло":

            raw_birth = db_query("SELECT birthdate FROM Users WHERE chat = ?", (mess.chat.id,), fetchone=True)
            date = raw_birth[0].split()
            listed_date = list(map(int, date[0].split("-")))
            birth_date = datetime.datetime(*listed_date)

            weeks_passed = (datetime.datetime.now() - birth_date).days // 7
            bot.send_message(mess.chat.id, f"Від вашого народження пройшло {weeks_passed} тижнів!")
        
        
        elif mess.text == "Cкільки днів пройшло":

            raw_birth = db_query("SELECT birthdate FROM Users WHERE chat = ?", (mess.chat.id,), fetchone=True)
            date = raw_birth[0].split()
            listed_date = list(map(int, date[0].split("-")))
            birth_date = datetime.datetime(*listed_date)

            weeks_passed = (datetime.datetime.now() - birth_date).days
            bot.send_message(mess.chat.id, f"Від вашого народження пройшло {weeks_passed} д{'ень' if weeks_passed % 10 == 1 else 'ні' if weeks_passed % 10 < 5 and weeks_passed % 10 == 0 else 'нів' }!")
        
        elif mess.text == "Змінити дату народження":
            db_query("DELETE FROM Users WHERE chat = ?", (mess.chat.id,), commit=True)
            bot.send_message(mess.chat.id, "Введіть нову дату народження в форматі\nдд.мм.рррр")


        else:
            bot.send_message(mess.chat.id, "Такої команди не існує")

bot.polling(none_stop=True)
