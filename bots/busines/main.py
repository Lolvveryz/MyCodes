import telebot, sys, os, time
from telebot import types
from dotenv import load_dotenv
from gpt import gpt4
from db import save_all_data, load_all_data
from people_chats import users
load_dotenv()
load_all_data(users)
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.business_message_handler(content_types=['photo', 'text'], func=lambda mess: mess.from_user.username!="lolvveryz")
def business_message(mess: types.Message):
    if mess.content_type == "text":
        response = gpt4(mess.text, os.getenv('API'), mess.from_user.id)
        bot.send_message(mess.chat.id, response, business_connection_id=mess.business_connection_id)  

bot.polling(non_stop=True)