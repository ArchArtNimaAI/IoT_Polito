import time
import telepot
import requests
import json
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# to take the chatid from Telegram API
# https://api.telegram.org/bot6372052902:AAH2eojNuFwzX3fgSrfSBHDSYh08aPpV4FE/getUpdates

token = "5905652798:AAGqKcD3mZrbyh0R7IlMSQft1XwbmHrV0aQ"
#chatid = 2059542548

class MyBOT():
    def __init__(self, token):#chatid):
        self.token = token
        self.bot = telepot.Bot(self.token)
        self.chatid =  'yo'
        self.callback_dict = {'chat': self.on_chat_message,
                              'callback_query': self.queries}

    def start(self):
        MessageLoop(self.bot, self.callback_dict).run_as_thread()

    def on_chat_message(self, msg):
        # print(msg)
        content_type, chat_type, chat_ID = telepot.glance(msg)
        command = msg['text']
        print(command)
        if command == '/on':
            print("turning on lights")
            # keyboard = InlineKeyboardMarkup(inline_keyboard=[
            # [InlineKeyboardButton(text='SwitchON', callback_data='ON'),
            #	InlineKeyboardButton(text='SwitchOFF', callback_data='OFF')]])
            # self.bot.sendMessage(chat_ID, text='What do you want to do', reply_markup=keyboard)
            res = requests.get("http://127.0.0.1:8099/on")
            res = json.loads(res)
            msg = "Result: " + res["status"]
            self.bot.sendMessage(self.chatid, text=msg)
        elif command == "/off":
            print("turning off lights")
            res = requests.get("http://127.0.0.1:8099/off")
            res = json.loads(res)
            msg = "Result: " + res["status"]
            self.bot.sendMessage(self.chatid, text=msg)
        elif command == "":
            msg = "Actions available:\n"
            msg += "/on	=> turn on the lights\n"
            msg += "/off => turn off the lights\n"
            msg += "/help => shows this help\n"
            self.bot.sendMessage(self.chatid, text=msg)

    def queries(self, msg):
        query_id, ch_id, query = telepot.glance(msg, flavor='callback_query')
        print(msg, '\n\n')
        if query == 'ON':
            body = {}
            request.put('url', body)
            self.client.publish()
    # if query


if __name__ == '__main__':
    bot = MyBOT(token) #chatid)
    bot.start()
    while True:
        time.sleep(1)
