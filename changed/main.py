import telebot , importlib , shutil , os


bot = telebot.TeleBot("6159454834:AAGtkISBzGFE8rBtD4Ksqy1YeBKRpqpSOL8")
ids = [661202949, 1583126842, 6187875959]
isNamed = False
directory = "D:\\Codes\\bot\\changed\\added"


status = {661202949 : False, # мій ip
          1583126842 : False}# твій ip

try:
    shutil.rmtree('D:\\Codes\\bot\\changed\\added')
    os.mkdir("D:\\Codes\\bot\\changed\\added")

except:
    os.mkdir("D:\\Codes\\bot\\changed\\added")

@bot.message_handler(commands=["start"])
def start(mess):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Тестування кодів"), telebot.types.KeyboardButton("Запит на розробника"))
    
    bot.send_message(mess.chat.id, "Вітаю у моєму боті , якщо ти зареєстрований у нас розробник , напиши /develop для створення коду , якщо ж корситувач , просто натисни на кнопку у себе в клавіатурі і протестуй коди наших розробників", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def main(mess):
    global isNamed, branch_name , status, directory

    if mess.chat.type == "private":
        id = mess.from_user.id
        chat = mess.chat.id

        if mess.text == "/develop":

            if id in ids:
                status[id] = not status[id]

                if status[id]:
                    bot.send_message(chat, "!розробка!\n*Що б вийти , напишіть /develop знову*")
                    bot.pin_chat_message(chat, mess.message_id+1)
                    bot.delete_message(chat, mess.message_id+2)
                    bot.send_message(chat, "Введи назву файлу нового коду")
                else:
                    bot.send_message(chat, "ви вийшли з розробки")
                    bot.unpin_all_chat_messages(chat)
            else:
                bot.send_message(chat, "не адмін")
                print(mess.from_user)

        elif mess.text == "/admin":
            with open("D:\\Codes\\bot\\changed\\main.py", "w"):
                pass #не дороблено , має змінюватись основниц прям код , не дороблено , взагалі тільки почав , якщо-що можеш видалити 53-55 строчки

        elif id in ids and status[id]:
            
            if isNamed:

                with open(f"D:\\Codes\\bot\\changed\\added\\{branch_name}", "w") as d:
                    d.write(mess.text)

                isNamed = not isNamed
                status[id] = not status[id]

                spec = importlib.util.spec_from_file_location(branch_name, f"D:\\Codes\\bot\\changed\\added\\{branch_name}")
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)

                m.changed(bot, mess)

                bot.send_message(chat, "код завершився , ви вийшли з розробки")
                bot.unpin_all_chat_messages(chat)
            else:
                def file_already_exist(name):
                    for root, dirs, files in os.walk(directory):
                        for file_name in files:
                            if file_name[:-3] == name:
                                bot.send_message(chat, "Файл з такою назвою вже існує , введіть іншу назву")
                                return(True)
                        break
                    return(False)
                
                if not file_already_exist(mess.text):
                    branch_name = mess.text+".py"
                    isNamed = not isNamed
                    bot.send_message(chat, "тепер введи код")

        else:
            if mess.text == "Тестування кодів":
                markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                for root, dirs, files in os.walk(directory):
                    for file_name in files:
                        markup.add(telebot.types.InlineKeyboardButton(file_name, callback_data=file_name))
                    break

                bot.send_message(chat, "вибери код", reply_markup=markup)
            elif mess.text == "Запит на розробника":
                pass


@bot.callback_query_handler(lambda call: True)
def callback(call):
    chat = call.message.chat.id

    spec = importlib.util.spec_from_file_location(call.data, f"D:\\Codes\\bot\\changed\\added\\{call.data}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    m.changed(bot, call.message)

    bot.send_message(chat, "код - все")

bot.polling(non_stop=True)
