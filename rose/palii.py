import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('YOUR_BOT_TOKEN')
admin_name = 'Ілля'
admin_password = 'SkkzGfksqDOLAR!@'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_auth = types.KeyboardButton('Авторизуватися')
    btn_reg = types.KeyboardButton('Зареєструватися')
    markup.add(btn_auth, btn_reg)
    bot.send_message(message.chat.id, 'Привіт, радий тебе бачити!', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == 'Зареєструватися')
def register(message):
    bot.send_message(message.chat.id, 'Введи свій нік:')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введіть пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('CYB.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50), role VARCHAR(20), tasks_week TEXT, tasks_day TEXT)')
    cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Ви успішно зареєстровані! Вітаємо в команді!')

@bot.message_handler(func=lambda m: m.text == 'Авторизуватися')
def auth(message):
    bot.send_message(message.chat.id, 'Введіть нік')
    bot.register_next_step_handler(message, check_name)

def check_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введіть пароль')
    bot.register_next_step_handler(message, check_pass, name)

def check_pass(message, name):
    password = message.text.strip()
    conn = sqlite3.connect('CYB.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = ? AND pass = ?", (name, password))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user:
        if name == admin_name and password == admin_password:
            admin_menu(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_yes = types.KeyboardButton('Так')
            btn_no = types.KeyboardButton('Ні')
            markup.add(btn_yes, btn_no)
            bot.send_message(message.chat.id, f'Привіт, {name}, заряджений на роботу?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введені дані не вірні')

def admin_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_assign_role = types.KeyboardButton('Призначити роль')
    btn_set_tasks = types.KeyboardButton('Встановити завдання')
    markup.add(btn_assign_role, btn_set_tasks)
    bot.send_message(message.chat.id, 'Адмін-меню', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == 'Призначити роль')
def assign_role(message):
    bot.send_message(message.chat.id, 'Введіть нік користувача')
    bot.register_next_step_handler(message, get_user_name_for_role)

def get_user_name_for_role(message):
    user_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введіть роль для користувача')
    bot.register_next_step_handler(message, set_user_role, user_name)

def set_user_role(message, user_name):
    role = message.text.strip()
    conn = sqlite3.connect('CYB.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = ? WHERE name = ?", (role, user_name))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Роль "{role}" успішно призначена для користувача "{user_name}"')



@bot.message_handler(func=lambda m: m.text == 'Встановити завдання')
def set_tasks(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_week_tasks = types.KeyboardButton('Завдання на тиждень')
    btn_day_tasks = types.KeyboardButton('Завдання на день')
    markup.add(btn_week_tasks, btn_day_tasks)
    bot.send_message(message.chat.id, 'Оберіть тип завдання', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == 'Завдання на тиждень')
def set_week_tasks(message):
    bot.send_message(message.chat.id, 'Введіть нік користувача')
    bot.register_next_step_handler(message, get_user_name_for_week_tasks)

def get_user_name_for_week_tasks(message):
    user_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введіть завдання на тиждень для користувача')
    bot.register_next_step_handler(message, save_week_tasks, user_name)

def save_week_tasks(message, user_name):
    tasks = message.text.strip()
    conn = sqlite3.connect('CYB.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET tasks_week = ? WHERE name = ?", (tasks, user_name))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Завдання на тиждень для користувача "{user_name}" встановлено')

@bot.message_handler(func=lambda m: m.text == 'Завдання на день')
def set_day_tasks(message):
    bot.send_message(message.chat.id, 'Введіть нік користувача')
    bot.register_next_step_handler(message, get_user_name_for_day_tasks)

def get_user_name_for_day_tasks(message):
    user_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введіть завдання на день для користувача')
    bot.register_next_step_handler(message, save_day_tasks, user_name)

def save_day_tasks(message, user_name):
    tasks = message.text.strip()
    conn = sqlite3.connect('CYB.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET tasks_day = ? WHERE name = ?", (tasks, user_name))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Завдання на день для користувача "{user_name}" встановлено')

@bot.message_handler(func=lambda m: m.text in ['Так', 'Ні'])
def handle_button(message):
    if message.text == 'Так':
        bot.send_message(message.chat.id, 'Красава, це по нашому!')
    else:
        bot.send_message(message.chat.id, 'Ти що ахуєл?')

bot.infinity_polling()
