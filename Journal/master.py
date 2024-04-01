import telebot
from telebot import types

from data import objects, token, user, temp, temp_calls
from funk import choise_object, start, master

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def start_master(message):
    if message.chat.type == "private":
        start(bot=bot, mess=message)


@bot.message_handler(content_types=['text'])
def main_master(message):
    if message.chat.type == "private":
        master(bot=bot, mess=message)


@bot.callback_query_handler(func=lambda call: True)
def calls_master(call):
    pass


bot.polling(non_stop=True)
