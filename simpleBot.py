import telepot
from telepot.loop import MessageLoop
import json
import requests
import time
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class MyBot:
	def __init__(self,token):
		# Local token
		self.tokenBot=token
		# Catalog token
		#self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
		self.bot=telepot.Bot(self.tokenBot)
		MessageLoop(self.bot,{'chat': self.on_chat_message}).run_as_thread()
		print(self.bot.getMe())
		exit()

		self.bot.sendMessage(5737459265, text="Welcome to MARGHE")

	def msg_handler(self,msg):
		content_type, chat_type, chat_ID = telepot.glance(msg)
		message = msg ['text']

	def on_chat_message(self,msg):
		content_type, chat_type, chat_ID = telepot.glance(msg)
		message = msg['text']
		if message == "/switch":
			buttons = [[InlineKeyboardButton(text=f'ON 🟡', callback_data=f'on'), 
					InlineKeyboardButton(text=f'OFF ⚪', callback_data=f'off')]]
			keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
			self.bot.sendMessage(chat_ID, text='What do you want to do', reply_markup=keyboard)
		else:
			self.bot.sendMessage(chat_ID, text="Command not supported")

if __name__ == '__main__':
	token = 'xxx'
	bot = MyBot(token)
	