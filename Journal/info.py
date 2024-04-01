import telebot
from telebot import types
bot = telebot.TeleBot("6159454834:AAGtkISBzGFE8rBtD4Ksqy1YeBKRpqpSOL8")

@bot.message_handler(content_types=['text'])
def m(mess):
    m = types.InlineKeyboardMarkup()
    a = types.InlineKeyboardButton("1", callback_data="1")
    m.add(a)
    bot.send_message(mess.chat.id, "1", reply_markup=m)

@bot.callback_query_handler(lambda call: True)
def call(call):
    if call.data == "1":
        bot.send_message(call.message.chat.id, call)
bot.polling(non_stop=True)