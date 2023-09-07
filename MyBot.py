import telepot
from telepot.loop import MessageLoop
import time
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from MyMQTT import *
class MyBOT():
	def __init__(self, token):
		self.token = token 
		self.bot = telepot.Bot(self.token)
		self.callback_dict = {'chat':self.on_chat_message,
							  'callback_query': self.queries}

	def start(self):
		MessageLoop(self.bot,self.callback_dict).run_as_thread()
		self.client
		
	def on_chat_message(self,msg):
		#print(msg)
		content_type, chat_type, chat_ID = telepot.glance(msg)
		command = msg['text'] 
		
			#do something else
		if command == '/light1':
			keyboard = InlineKeyboardMarkup(inline_keyboard=[
    		[InlineKeyboardButton(text='SwitchON', callback_data='ON'),
     			InlineKeyboardButton(text='SwitchOFF', callback_data='OFF')]])
			self.bot.sendMessage(chat_ID, text='What do you want to do', reply_markup=keyboard)



	def queries(self,msg):
		query_id, ch_id, query = telepot.glance(msg, flavor='callback_query')
		print(msg, '\n\n')
		if query == 'ON':
			body={}
			request.put('url',body)
			self.client.publish()
		#if query



if __name__ == '__main__':
	token= 'xxx'
	bot = MyBOT(token)
	bot.start()
	while True:
		time.sleep(1)