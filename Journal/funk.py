import telebot
from data import temp, user
from site_attraction import main

def choise_object(bot, mess, objects, temp_calls):
    bot.send_message(mess.chat.id, "Виберіть предмет",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    id_ = mess.message_id
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    calls = 0
    for obj, value in objects.items():

        temp_calls[str(calls)] = obj
        add = telebot.types.InlineKeyboardButton(obj, callback_data=str(calls))
        markup.add(add)
        calls += 1
    bot.send_message(mess.chat.id, "Ваші предмети", reply_markup=markup)
    return id_

register_proces = False

def start(bot, mess):
    chat = mess.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=2)
    markup.add(telebot.types.KeyboardButton("Реєстрація"),
               telebot.types.KeyboardButton("Вхід"))

    bot.send_message(chat_id=chat, text="Вітаю у моєму боті з журналом", reply_markup=markup)


def master(bot, mess):
    global register_proces 

    chat = mess.chat.id
    text = mess.text
    user_id = mess.from_user.id

    if register_proces:
        register_proces = registration(text=text, user_id=user_id, bot=bot, mess=mess)
            
    else :
        if text == "Реєстрація":
            register_proces = True
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_message(chat, "Введіть пошту і пароль прив'язані до журналу <u>окремими повідомленнями</u>", reply_markup=markup, parse_mode = 'html' )
        elif text == "Вхід":
            pass

def after_verification(bot, mess):
    chat = mess.chat.id
    if main():
        bot.send_message(chat, "Успішно верифіковано!")
    else:
        bot.send_message(chat, "Хуйня!")


def registration(text, user_id, bot, mess):
    if not user_id in temp.keys():
        temp[user_id] = [text]
        return True
    else :
        temp[user_id].append(text)
        user["username"] = temp[user_id][0]
        user["password"] = temp[user_id][1]
        after_verification(bot=bot, mess=mess)
        return False