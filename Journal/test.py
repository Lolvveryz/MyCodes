import telebot

bot = telebot.TeleBot("6159454834:AAGtkISBzGFE8rBtD4Ksqy1YeBKRpqpSOL8")

@bot.message_handler()
def main(mess):
    user = ["MaxB2006"]
    if mess.from_user.username in user :
        bot.set_message_reaction(mess.chat.id, mess.message_id, [telebot.types.ReactionTypeEmoji("👎")])


bot.polling(non_stop=True)
