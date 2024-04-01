import telebot
from data import token
bot = telebot.TeleBot(token)

@bot.message_handler()
def main(mess):
    user = ["MaxB2006"]
    if mess.from_user.username in user :
        bot.set_message_reaction(mess.chat.id, mess.message_id, [telebot.types.ReactionTypeEmoji("👎")])


bot.polling(non_stop=True)
