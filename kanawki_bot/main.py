import telebot

bot = telebot.TeleBot("5964862187:AAEuCxmO-pB0eEv8ZlVPYJfs-3QcYJ8S-kQ")

@bot.message_handler(commands=["start", "login"])
def commands(mess):
    
    if mess.text == "/start":
        bot.send_message(mess.chat.id, "Привіт\nПройди реєстрацію :\nІм'я корситувача\nПароль")