import keyboard, time
from  request import geter
def code():
    mess = geter().split()
    
    print("Переходьте на сайт і натискайте Enter")

    for i in range(len(mess)):
        keyboard.write(mess[i])
        if mess[i] is not mess[-1]:
            keyboard.send('space')
    time.sleep(1)

    print("Код завершив роботу, що б продовжити , натисніть Enter, або вручну вимкніть код")
 
while True:
    keyboard.wait("Enter") # клавіша запуску коду
    code()
    