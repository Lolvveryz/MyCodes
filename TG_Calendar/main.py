import sqlite3
import datetime
import telebot
from telebot import types

bot = telebot.TeleBot()


def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat INTEGER NOT NULL,
                username TEXT NOT NULL
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


def create_user_table(user_id):
    table_name = f"user_{user_id}"

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status INTEGER NOT NULL DEFAULT 0,
                deadline TIMESTAMP,
                priority INTEGER NOT NULL,
                types TEXT NOT NULL
            )
        ''')
        conn.commit()


def start_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    create = types.KeyboardButton("Створити подію")
    check = types.KeyboardButton("Мої події/редагувати")
    markup.add(create, check)
    return markup


def get_title(message):
    ask_desc = bot.send_message(message.chat.id, "Введіть опис події! \n\n0 якщо хочете залишити пустим")
    bot.register_next_step_handler(ask_desc, get_desc, message.text)


def get_desc(message, title=None):
    desc = None if message.text == "0" else message.text

    # markup = types.InlineKeyboardMarkup(row_width=7)
    #
    # a1 = types.InlineKeyboardButton("1", callback_data="day|1")
    # a2 = types.InlineKeyboardButton("2", callback_data="day|2")
    # a3 = types.InlineKeyboardButton("3", callback_data="day|3")
    # a4 = types.InlineKeyboardButton("4", callback_data="day|4")
    # a5 = types.InlineKeyboardButton("5", callback_data="day|5")
    # a6 = types.InlineKeyboardButton("6", callback_data="day|6")
    # a7 = types.InlineKeyboardButton("7", callback_data="day|7")
    #
    # b1 = types.InlineKeyboardButton("8", callback_data="day|8")
    # b2 = types.InlineKeyboardButton("9", callback_data="day|9")
    # b3 = types.InlineKeyboardButton("10", callback_data="day|10")
    # b4 = types.InlineKeyboardButton("11", callback_data="day|11")
    # b5 = types.InlineKeyboardButton("12", callback_data="day|12")
    # b6 = types.InlineKeyboardButton("13", callback_data="day|13")
    # b7 = types.InlineKeyboardButton("14", callback_data="day|14")
    #
    # c1 = types.InlineKeyboardButton("15", callback_data="day|15")
    # c2 = types.InlineKeyboardButton("16", callback_data="day|16")
    # c3 = types.InlineKeyboardButton("17", callback_data="day|17")
    # c4 = types.InlineKeyboardButton("18", callback_data="day|18")
    # c5 = types.InlineKeyboardButton("19", callback_data="day|19")
    # c6 = types.InlineKeyboardButton("20", callback_data="day|20")
    # c7 = types.InlineKeyboardButton("21", callback_data="day|21")
    #
    # d1 = types.InlineKeyboardButton("22", callback_data="day|22")
    # d2 = types.InlineKeyboardButton("23", callback_data="day|23")
    # d3 = types.InlineKeyboardButton("24", callback_data="day|24")
    # d4 = types.InlineKeyboardButton("25", callback_data="day|25")
    # d5 = types.InlineKeyboardButton("26", callback_data="day|26")
    # d6 = types.InlineKeyboardButton("27", callback_data="day|27")
    # d7 = types.InlineKeyboardButton("28", callback_data="day|28")
    #
    # e1 = types.InlineKeyboardButton("29", callback_data="day|29")
    # e2 = types.InlineKeyboardButton("30", callback_data="day|30")
    # e3 = types.InlineKeyboardButton("31", callback_data="day|31")
    #
    # empty = types.InlineKeyboardButton(" ", callback_data="day|0")
    #
    # markup.add(a1, a2, a3, a4, a5, a6, a7)
    # markup.add(b1, b2, b3, b4, b5, b6, b7)
    # markup.add(c1, c2, c3, c4, c5, c6, c7)
    # markup.add(d1, d2, d3, d4, d5, d6, d7)
    # markup.add(e1, e2, e3, empty, empty, empty, empty)

    ask_deadline = bot.send_message(message.chat.id, "Введіть дедлайн/дату задачі/події!"
                                                     "\nформат : дд.мм.рр(якщо весь день)"
                                                     "\n                  дд.мм.рр год:хв"
                                                     "\n\n0 якщо хочете залишити пустим")
    bot.register_next_step_handler(ask_deadline, get_deadline, title, desc)


def get_deadline(message, title=None, desc=None):
    if message.text == "0":
        date = None
    else:
        text = message.text.split(" ")

        if len(text) == 1:
            day = text[0].split(".")
            if len(day) == 3:
                try:
                    date = datetime.date(int(day[2]), int(day[1]), int(day[0]))
                except ValueError:
                    back = bot.send_message(message.chat.id, "Некоректна дата! Спробуйте ще раз.")
                    bot.register_next_step_handler(back, get_deadline, title, desc)
                    return
            else:
                back = bot.send_message(message.chat.id, "Неправильний формат! Спробуйте ще раз.")
                bot.register_next_step_handler(back, get_deadline, title, desc)
                return

        elif len(text) == 2:
            day = text[0].split(".")
            time = text[1].split(":")
            if len(day) == 3 and len(time) == 2:
                try:
                    date = datetime.datetime(int(day[2]), int(day[1]), int(day[0]), int(time[0]), int(time[1]))
                except ValueError:
                    back = bot.send_message(message.chat.id, "Некоректна дата! Спробуйте ще раз.")
                    bot.register_next_step_handler(back, get_deadline, title, desc)
                    return
            else:
                back = bot.send_message(message.chat.id, "Неправильний формат! Спробуйте ще раз.")
                bot.register_next_step_handler(back, get_deadline, title, desc)
                return
        else:
            back = bot.send_message(message.chat.id, "Неправильний формат! Спробуйте ще раз.")
            bot.register_next_step_handler(back, get_deadline, title, desc)
            return
    ask_priority = bot.send_message(message.chat.id,
                                    "Введіть пріоритет події , де \n0 - не в пріоритеті\n20 - макисмальний пріоритет !")
    bot.register_next_step_handler(ask_priority, get_priority, title, desc, date)


def get_priority(message, title=None, desc=None, deadline=None):
    try:
        if int(message.text) < 0:
            back = bot.send_message(message.chat.id, "Пріоритет не можe бути меньше нуля! Спробуйте ще раз.")
            bot.register_next_step_handler(back, get_priority, title, desc, deadline)
            return
        elif int(message.text) > 20:
            back = bot.send_message(message.chat.id, "Занадто високий пріоритет! Спробуйте ще раз.")
            bot.register_next_step_handler(back, get_priority, title, desc, deadline)
            return
    except ValueError:
        back = bot.send_message(message.chat.id, "Пріоритет вводиться цифрами! Спробуйте ще раз.")
        bot.register_next_step_handler(back, get_priority, title, desc, deadline)
        return

    markup = types.ReplyKeyboardMarkup(row_width=1)
    task = types.KeyboardButton("Задача")
    plan = types.KeyboardButton("Подія")
    markup.add(task, plan)

    ask_type = bot.send_message(message.chat.id, "Виберіть тип події", reply_markup=markup)
    bot.register_next_step_handler(ask_type, add_event, title, desc, deadline, int(message.text))


def add_event(message, title=None, desc=None, deadline=None, priority=None):
    if message.text not in ["Задача", "Подія"]:

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        task = types.KeyboardButton("Задача")
        plan = types.KeyboardButton("Подія")
        markup.add(task, plan)

        back = bot.send_message(message.chat.id, "Оберіть кнопкою!", reply_markup=markup)
        bot.register_next_step_handler(back, add_event, title, desc, deadline, priority)
    else:
        event_type = "event" if message.text == "Подія" else "task"
        table_name = f"user_{message.from_user.id}"

        db_query(f"INSERT INTO {table_name} (title, description, deadline, priority, types) VALUES (?, ?, ?, ?, ?)",
                 (title, desc, deadline, priority, event_type),
                 commit=True)
        bot.send_message(message.chat.id, "ДОДАНО", reply_markup=start_markup())


def get_types(task="Задача", event="Подія", activate=None):
    markup = types.InlineKeyboardMarkup()
    task = types.InlineKeyboardButton(text=task, callback_data="sort|task")
    event = types.InlineKeyboardButton(text=event, callback_data="sort|event")

    markup.add(task, event, row_width=2)
    markup.add(types.InlineKeyboardButton("Обрати", callback_data=f"sort|pick|{activate}"))
    return markup


def get_sort(priority="За пріоритетом", date="По даті", activate1=None, activate2=None, ):
    markup = types.InlineKeyboardMarkup(row_width=1)
    priority = types.InlineKeyboardButton(text=priority, callback_data=f"sort|priority|{activate1}")
    date = types.InlineKeyboardButton(text=date, callback_data=f"sort|date|{activate1}")

    markup.add(priority, date, row_width=2)
    markup.add(types.InlineKeyboardButton("Обрати", callback_data=f"sort|pick|{activate1}|{activate2}"))
    return markup


def sort_by_date(type, id):
    table_name = f"user_{id}"
    query = f"""
    SELECT * FROM {table_name}
    WHERE types = ?
    ORDER BY deadline"""
    return db_query(query, (type,), fetchall=True)


def sort_by_priority(type, id):
    table_name = f"user_{id}"
    query = f"""
        SELECT * FROM {table_name}
        WHERE types = ?
        ORDER BY priority DESC"""
    return db_query(query, (type,), fetchall=True)


def raw_to_beautiful(raw):
    date = raw[4].split(" ")
    date[0] = date[0].split("-")
    date[0][0] = f"20{date[0][0][2:]}"

    beautiful = [raw[1], raw[2], f"{date[0][1]}/{date[0][2]}/{date[0][0]} {date[1] if len(date) == 2 else ''}", raw[5]]
    backend = [raw[0], raw[3], raw[6]]
    return [beautiful, backend]


@bot.message_handler(commands=['start'])
def start(message):
    # Перевірка, чи користувач вже зареєстрований
    fetched_data = db_query("SELECT id FROM Users WHERE chat = ?",
                            (message.from_user.id,), fetchone=True)

    if fetched_data is None:
        # Перевірка username, якщо він відсутній - встановлюємо "anonymous"
        username = message.from_user.username or "anonymous"
        db_query("INSERT INTO Users (chat, username) VALUES (?, ?)",
                 (message.chat.id, username), commit=True)

        create_user_table(message.from_user.id)

        bot.send_message(message.chat.id,
                         f"Привіт, {username}!\n\nЯ допоможу тобі з плануванням та нагадуванням твоїх справ або подій!",
                         reply_markup=start_markup())
    else:
        bot.send_message(message.chat.id, "Вже зареєстровано", reply_markup=start_markup())


@bot.message_handler(content_types=['text'])
def main(mess):
    if mess.text == "Створити подію":
        bot.send_message(mess.chat.id, "Ви введете наступні дані:"
                                       "\n\nНазва події (обов'язково)"
                                       "\nОпис події (необов'язково)"
                                       "\nДедлайн/дата події (необов'язково)"
                                       "\nПріоритетність події (необов'язково)"
                                       "\nТип події (завдання/подія)")
        ask_title = bot.send_message(mess.chat.id, "Введіть назву для вашої події",
                                     reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(ask_title, get_title)

    elif mess.text == "Мої події/редагувати":
        markup = get_types()
        bot.send_message(mess.chat.id, "Виберіть що сортувати :", reply_markup=markup)


# Колбек для вказівок щодо сортування ЩО і ЯК сортувати
@bot.callback_query_handler(lambda call: call.data.startswith("sort"))
def callback_to_look(call):
    data = call.data.split("|")
    if data[1] == "task":
        bot.edit_message_text("Виберіть що сортувати :", call.message.chat.id, call.message.message_id,
                              reply_markup=get_types(task="Задача✅", activate="task"))
    if data[1] == "event":
        bot.edit_message_text("Виберіть що сортувати :", call.message.chat.id, call.message.message_id,
                              reply_markup=get_types(event="Подія✅", activate="event"))
    if data[1] == "priority":
        bot.edit_message_text("Виберіть як сортувати :", call.message.chat.id, call.message.message_id,
                              reply_markup=get_sort(priority="За пріоритетом✅", activate1=data[2],
                                                    activate2="priority"))
    if data[1] == "date":
        bot.edit_message_text("Виберіть як сортувати :", call.message.chat.id, call.message.message_id,
                              reply_markup=get_sort(date="По даті✅", activate1=data[2], activate2="date"))
    if data[1] == "pick":
        if len(data) == 3:
            if data[2] in ["task", "event"]:
                bot.edit_message_text(f"Виберіть як сортувати :", call.message.chat.id, call.message.message_id,
                                      reply_markup=get_sort(activate1=data[2]))
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Виберіть завдання чи подію!')

        elif data[3] is not None:
            bot.edit_message_text(f"Ви сортуєте {data[2]}, за {data[3]}", call.message.chat.id, call.message.message_id)

            if data[3] == "priority":
                db_data = sort_by_priority(data[2], call.from_user.id)

                for i in db_data:
                    raw = raw_to_beautiful(i)
                    for_user = raw[0]
                    backend = raw[1]
                    to_sand = (f"Назва : {for_user[0]}\n"
                               f"Опис : {for_user[1] if for_user[1] is not None else 'Опис відсутній'}\n"
                               f"Дедлайн : {for_user[2] if for_user[2] is not None else 'Дедлайн відcутній'}\n"
                               f"Пріорітет : {for_user[3]}\n")

                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if data[2] == "task":
                        check = types.InlineKeyboardButton("Виконати", callback_data=f"check|{backend[0]}|{call.message.message_id}")
                        markup.add(check)
                    edit = types.InlineKeyboardButton(f"Редагувати, {backend[0]}", callback_data=f"edit|{backend[0]}|{call.message.message_id}")
                    delete = types.InlineKeyboardButton("Видалити", callback_data=f"delete|{backend[0]}|{call.message.message_id}")
                    markup.add(edit, delete)

                    bot.send_message(call.message.chat.id, to_sand, reply_markup=markup)
            elif data[3] == "date":
                pass
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Виберіть метод сортування!')


# Колбек для завдань , для змінення їх на виконано
@bot.callback_query_handler(lambda call: call.data.startswith("check"))
def callback_to_edit_task(call):
    data = call.data.split("|")


# Колбек для редагування значень події/задачі
@bot.callback_query_handler(lambda call: call.data.startswith("edit"))
def callback_to_edit(call):
    data = call.data.split("|")


# Колбек для видалення подій/задач
@bot.callback_query_handler(lambda call: call.data.startswith("delete"))
def callback_to_delete(call):
    data = call.data.split("|")
    

bot.polling(non_stop=True)
