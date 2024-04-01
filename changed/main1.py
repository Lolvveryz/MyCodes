# не дороблено і не пам'ятаю що має бути
def changed_main(mess, bot, chat, directory):
    if mess.text == "Тестування кодів":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                markup.add(telebot.types.InlineKeyboardButton(file_name, callback_data=file_name))
            break

        bot.send_message(chat, "вибери код", reply_markup=markup)
    elif mess.text == "Запит на розробника":
        pass
