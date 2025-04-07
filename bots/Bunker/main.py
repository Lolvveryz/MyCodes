import telebot
from telebot import types
from private import private
from groups import group
import data
bot = telebot.TeleBot(data.api)


@bot.message_handler(content_types=['text'])
def main(mess):
    if mess.chat.type == "private":
        private(mess)
    else :
        group(mess)


@bot.callback_query_handler(lambda call: True)
def callback(call):
    if data.mes == 0:
        data.mes = call.message.id
    match call.data:
        case "reg":
            len1 = len(data.players)
            data.players[call.from_user.id] = ""
            if len1 != len(data.players):
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Реєстрація", callback_data="reg"))

                data.text += " "+(f"@{call.from_user.username}") if call.from_user.username != None else " "+call.from_user.first_name
                
                bot.edit_message_text(data.text, call.message.chat.id, data.mes, reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, f"{data.players}\n\n{call.from_user.id}-{call.from_user.username}")
                bot.answer_callback_query(callback_query_id=call.id, text='Ви вже зареєстровані')



bot.polling(non_stop=True)