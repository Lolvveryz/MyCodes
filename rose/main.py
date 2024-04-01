from data import bot , users
from User import User
from telebot import types

import pprint

@bot.message_handler(commands=['start'])
def start(message):
    # Створення об'єкта користувача
    user = User(message)

    # Збереження об'єкта користувача у словнику
    users[str(message.from_user.id)] = user

    bot.reply_to(message, f"{message.from_user.username} - {message.from_user.id}")

    
@bot.message_handler()
def main(mess):
    if mess.text == "/mess":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for _id in users.keys():
            typ = types.InlineKeyboardButton(str(_id), callback_data=str(_id))
            markup.add(typ)
        bot.send_message(mess.chat.id, "Вибери кому відправити", reply_markup=markup)

    

@bot.callback_query_handler(func=lambda call: True)
def calls_master(call):
    if call.data in [user for user, value in users.items()]:
        users[call.data].send("УРА БЛЯТЬ")
    

if __name__ == "__main__":
    bot.polling()
