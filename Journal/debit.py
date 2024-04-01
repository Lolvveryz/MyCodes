import telebot
from telebot import types

bot = telebot.TeleBot("6159454834:AAGtkISBzGFE8rBtD4Ksqy1YeBKRpqpSOL8")


def check(odd, even, mess):    
    for i in range(len(odd)):
        temp = int(odd[i]) * 2
        if temp > 9:
            odd[i] = str(temp - 9)
        else:
            odd[i] = temp                    
    if sum([int(i) for i in odd]) + sum([int(i) for i in even]) % 10 ==0:
        bot.send_message(mess.chat.id, "Правильно!")
    else :
        bot.send_message(mess.chat.id, "Неправильно")

                        
@bot.message_handler(content_types=["text"])
def main(mess):
    if mess.text == "/start":
        bot.send_message(mess.chat.id, "Вітаю у боті валідації картки!\nВведіть картку")
    else:
        card = (mess.text).replace(" ", "")
        if not card.isdigit():
            bot.send_message(mess.chat.id, "УВАГА ЗНАЙДЕНО БУКВИИИИ")
        else :
            odd = [i for i in card[::2]]
            even = [i for i in card[1::2]]
            if len(card)%2-1 != 0:
                check(odd, even, mess)
            else : check(even, odd, mess)
                



bot.polling(non_stop=True)