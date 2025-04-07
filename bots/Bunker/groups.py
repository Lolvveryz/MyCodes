import telebot, time
from telebot import types
from person import Person
import data, random

bot = telebot.TeleBot(data.api)

katastrofa = {"Засуха: Усі водойми висохли, дощі припиняються на десятки років.", "Мутації: Радіаційний вибух спричинив появу небезпечних мутантів.", "Зомбі-вірус: Епідемія перетворює людей на агресивних істот.", "Виверження вулканів: Попіл закрив небо, рослини більше не ростуть.", "Повінь: Світ майже повністю покритий водою, суші дуже мало.", "Глобальне потепління: Температура піднялася до +70°C, повітря стає токсичним.", "Ядерна війна: Вся поверхня Землі забруднена радіацією.", "Метеорит: Удар знищив більшість континентів, пил перекрив сонце.", "Біологічна війна: Створений у лабораторії вірус вбив більшість населення.", "Астероїд: Велетенський метеорит зруйнував частину планети, залишивши хмари пилу.", "Глобальна пандемія: Смертельна хвороба поширилась через повітря.", "Радіоактивний вибух: Зараження перетворило людей і тварин на мутантів.", "Кліматичні зміни: Сніг покриває всю планету, температура впала до -60°C.", "Кіберкатастрофа: Роботи повстали проти людства.", "Космічна загроза: Інопланетна раса напала на Землю."}

def set_m(bot, mess):
    bot.delete_message(mess.chat.id, data.mes)
    bot.delete_message(mess.chat.id, data.mes-1)
    bot.delete_message(mess.chat.id, mess.id)
    data.mes = 0
    data.text = "Зареєстровані :\n"


def group(mess):
    
    if mess.text == "/bunker" or mess.text == "/bunker@shuuurick_bot":
        bot.send_message(mess.chat.id, players)
        if not data.players or data.players[0] == 0:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Реєстрація", callback_data="reg"))
            data.players[0]=0
            bot.send_message(mess.chat.id, "Реєстрація", reply_markup=markup)
        else:
            bot.delete_message(mess.chat.id, mess.id)


    elif mess.text == "/users" or mess.text == "/users@shuuurick_bot":
        bot.send_message(mess.chat.id, data.players)

    elif mess.text == "/start" or mess.text == "/start@shuuurick_bot":
        set_m(bot, mess)

        if len(data.players) > 0:
            bot.send_message(mess.chat.id, "Початок гри")
            bot.send_message(mess.chat.id, list(katastrofa)[random.randint(0, len(katastrofa)-1)])
            for _id,n in data.players.items():
                if _id:
                    data.players[_id] = Person(_id, (f"@{mess.from_user.username}") if mess.from_user.username != None else mess.from_user.first_name)
                    user = data.players[_id].get()
                    text = f'{user["username"]}\n\n💼Професія - {user["profession"]}\n👤Стать та вік - {user["biology"]}\n🎮Хобі - {user["hobi"]}\n📦Багаж - {user["bagazh"]}\n🩻Здоров\'я - {user["heal"]}\n📌Факти - {user["fakti"]}\n‼️Особливі умови - {user["bunker"]}'
                    bot.send_message(_id, text)
                    print()

        else :
            bot.send_message(mess.chat.id, "Замало гравців")
            data.players.clear

    elif mess.text == "/end" or mess.text == "/end@shuuurick_bot":
        data.players = {}
