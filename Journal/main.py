import telebot
from telebot import types

from data import objects, token, user, temp, temp_calls
from funk import choise_object
from site_attraction import main

bot = telebot.TeleBot(token)

registration_proces = False

@bot.message_handler(commands=['start'])
def start(mess):
    
    if mess.chat.type == "private":
        global registration_proces
        markup = types.InlineKeyboardMarkup()
        registration = types.InlineKeyboardButton(
            "Зареєструватись", callback_data="registration")              # 1
        markup.add(registration)
        bot.send_message(mess.chat.id, "Вітаю у моєму боті!", reply_markup=markup)
        registration_proces = True
    else :
        # bot.copy_message(mess.chat.id, mess.chat.id, mess.message_id)
        bot.reply_to(mess, "Ти реально хочеш всім свій журанл показувати? погана ідея..")


@bot.message_handler(content_types=['text'])
def master(mess):
    if mess.chat.type == "private":
        global registration_proces
        if registration_proces:
            if mess.from_user.id in temp:
                temp[mess.from_user.id].append(mess.text)
                if len(temp[mess.from_user.id]) == 2:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    confirm = types.InlineKeyboardButton(
                        "Підтвердити", callback_data="accept")                             # 3
                    deny = types.InlineKeyboardButton(
                        "Змінити", callback_data="deny")
                    markup.add(confirm, deny)
                    bot.send_message(
                        mess.chat.id, "Підтвердити дані?", reply_markup=markup)
            else:
                temp[mess.from_user.id] = [mess.text]

        else:
            if mess.text == "Оцінки":
                m = choise_object(bot, mess, objects, temp_calls)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global temp_calls
    global registration_proces
    if call.data == 'registration':
        bot.edit_message_text("Надішліть свою пошту та пароль окремими повідомленнями : ",
                              call.message.chat.id, call.message.message_id)    # 2
    elif call.data == "accept":

        user["username"] = temp[call.from_user.id][0]
        user["password"] = temp[call.from_user.id][1]

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id-2)
        bot.delete_message(call.message.chat.id, call.message.message_id-3)
        temp[call.from_user.id].clear()
        if main():
            registration_proces = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            marks = types.KeyboardButton("Оцінки")
            markup.add(marks)
            bot.send_message(call.message.chat.id,
                             "Успіх!", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                "Ввести дані ще раз", callback_data="again"))

            bot.send_message(
                call.message.chat.id, "Неправильний логін чи пароль :(", reply_markup=markup)

    elif call.data == "deny":
        [bot.delete_message(call.message.chat.id,
                            call.message.message_id-i) for i in range(4)]
        bot.send_message(
            call.message.chat.id, "Надішліть свою пошту та пароль окремими повідомленнями : ")
        temp[call.from_user.id].clear()

    elif call.data in temp_calls:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(
            "Повернутись до предметів", callback_data="back")
        markup.add(back)

        text = [f"{list(objects[temp_calls[call.data]][i].keys())[0]} - {objects[temp_calls[call.data]][i][list(
            objects[temp_calls[call.data]][i].keys())[0]]}" for i in range(len(objects[temp_calls[call.data]])) if i > 1]

        bot.send_message(call.message.chat.id, f"""{temp_calls[call.data]}\n№ {objects[temp_calls[call.data]][0]["№"]} - {objects[temp_calls[call.data]][1]["Студент"]}\n
{"\n".join([e for e in text])}""", reply_markup=markup)
        temp_calls.clear()

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id-2)
        choise_object(bot, call.message, objects, temp_calls)

    elif call.data == "again":

        bot.delete_message(call.message.chat.id, call.message.message_id)
        temp[call.from_user.id].clear()        
        bot.send_message(
            call.message.chat.id, "Надішліть свою пошту та пароль окремими повідомленнями : ")
        mess_to_delete = call.message.message_id


bot.polling(non_stop=True)
