import telebot, data
bot = telebot.TeleBot(data.api)

def private(mess):
    bot.send_message(mess.chat.id, "приватні повідомлення")


