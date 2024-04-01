import telebot
from DATA.data import Kanavki
bot = telebot.TeleBot(Kanavki.token)

@bot.message_handler(commands=["start", "login"])
def commands(mess):
    
    if mess.text == "/start":
        bot.send_message(mess.chat.id, "Привіт\nПройди реєстрацію :\nІм'я корситувача\nПароль")