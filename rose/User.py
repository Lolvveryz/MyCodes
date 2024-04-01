from data import bot

class User:
    def __init__(self, mess):
        self.id = mess.from_user.id
        self.mess = mess
        self.username = mess.from_user.username
    
    def info(self):
        return [self.id , self.username]
    
    def send(self, mess):
        bot.send_message(self.mess.chat.id, mess)

    