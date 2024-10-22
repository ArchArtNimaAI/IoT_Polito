import os
import time
import telepot
import requests
import json
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


token = "5905652798:AAGqKcD3mZrbyh0R7IlMSQft1XwbmHrV0aQ"


class MyBOT():
    def __init__(self, token):
        self.token = token
        self.bot = telepot.Bot(self.token)
        self.callback_dict = {'chat': self.on_chat_message,
                              'callback_query': self.queries}
        self.time = None
        self.user_state = {}


    def get_current_time(self):
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M')
        return self.time

    def save_updated_catalog(self, file):
        files = os.listdir()
        catalog_files = sorted([f for f in files if f.startswith('catalog_updated') and f.endswith('.json')])

        if catalog_files:
            last_file = catalog_files[-1]
            try:
                # Extracting the count from the filename
                last_count = int(last_file[len('catalog_updated'):-5])
            except ValueError:
                print(f"Unexpected filename format: {last_file}")
                last_count = 0
        else:
            last_count = 0

        last_count += 1  # Incrementing the count here

        new_file_path = f'catalog_updated{last_count}.json'
        with open(new_file_path, 'w') as u:
            json.dump(file, u, indent=4)

        return new_file_path  # Returning the path of the saved fil


    def send_catalog(self, chat_id, file_path):
        with open(file_path, 'rb') as file:
            self.bot.sendDocument(chat_id, file)

    def start(self):
        MessageLoop(self.bot, self.callback_dict).run_as_thread()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        command = msg['text']

        if command == '/start':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Control Light', callback_data='control_light'),
             InlineKeyboardButton(text='Update Catalog', callback_data='update_catalog')],
                [InlineKeyboardButton(text='light Status', callback_data='light_status'),
                 InlineKeyboardButton(text='Move Status', callback_data='move_status')]
            ])
            self.bot.sendMessage(chat_ID, text='What do you want to do?', reply_markup=keyboard)

# -----------------------------------------------------------------
# Add sections
# -----------------------------------------------------------------
        elif self.user_state[chat_ID] == 'Waiting_add_id':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['sensorId'].append(command)
            file['lastUpdate'] = self.get_current_time()
            self.save_updated_catalog(file)

            # Saveing the catalog
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]
            # Send it to the user
            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_sensor_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['sensorType'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_measuretype':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['measureType'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_service_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceType'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_service_ip':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceIP'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_topic':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['topic'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_actuator_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['Actuator']['Actuator_Type'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_add_actuator_properties':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['Actuator']['Properties']['Type'].append(command)
            file['lastUpdate'] = self.get_current_time()
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

# -----------------------------------------------------------------
#Remove sections
#-----------------------------------------------------------------
        elif self.user_state[chat_ID] == 'Waiting_remove_id':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['sensorId'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_remove_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['sensorType'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')


        elif self.user_state[chat_ID] == 'Waiting_remove_measureType':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['measureType'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_service_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceType'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_service_ip':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceIP'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_topic':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['sensor']['servicesDetails']['topic'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_actuator_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['Actuator']['Actuator_Type'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

        elif self.user_state[chat_ID] == 'Waiting_remove_properties':
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            file['rooms']['room1'][0]['Actuator']['Properties']['Type'].pop((int(command) - 1))
            new_file_path = self.save_updated_catalog(file)
            del self.user_state[chat_ID]

            self.send_catalog(chat_ID, new_file_path)
            self.bot.sendMessage(chat_ID, text='Catalog updated seccessfully!')

# -----------------------------------------------------------------
# Query section
# -----------------------------------------------------------------


    def queries(self, msg):
        query_id, ch_id, query = telepot.glance(msg, flavor='callback_query')
        print(msg, '\n\n')

        if query == 'control_light':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Room 1', callback_data='room_1_Light')],
                [InlineKeyboardButton(text='Room 2', callback_data='room_2_Light')],
                [InlineKeyboardButton(text='Room 3', callback_data='room_3_Light')]
            ])
            self.bot.sendMessage(ch_id, text='Which room would you like to control?(Which room would you like to update?\n'
                                             '(Please consider currently Room_1 has been activated)', reply_markup=keyboard)

        elif query == 'update_catalog':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Room 1', callback_data='room_1')],
                [InlineKeyboardButton(text='Room 2', callback_data='room_2')],
                [InlineKeyboardButton(text='Room 3', callback_data='room_3')]
            ])
            self.bot.sendMessage(ch_id, text='Which room would you like to update?(Please consider currently Room_1\n'
                                             ' has been activated)', reply_markup=keyboard)

        elif query in ['room_1_Light', 'room_2_Light', 'room_3_Light']:
            if query == 'room_1_Light':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='switchON', callback_data='on'),
                     InlineKeyboardButton(text='switchOFF', callback_data='off')]
                ])
                self.bot.sendMessage(ch_id, text='Choose an option:', reply_markup=keyboard)
            else:
                self.bot.sendMessage(ch_id, text='Sorry! This room info is not ready.')

        elif query == 'light_status':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Room 1', callback_data='room1_light_status')],
                [InlineKeyboardButton(text='Room 2', callback_data='room2_light_status')],
                [InlineKeyboardButton(text='Room 3', callback_data='room3_light_status')]
            ])
            self.bot.sendMessage(ch_id, text='Which room would you like to check light status?(Please consider currently Room_1\n'
                                             ' has been activated)', reply_markup=keyboard)

        elif query in ['room1_light_status', 'room2_light_status', 'room3_light_status']:
            if query == 'room1_light_status':
                url = 'http://127.0.0.1:8081/light-status'
                response = requests.get(url)
                if response.text == "on":
                    self.bot.sendMessage(ch_id, text='Status of light inside Room 1 is ON now!')
                else:
                    self.bot.sendMessage(ch_id, text='Status of light inside Room 1 is OFF now!.')
            else:
                self.bot.sendMessage(ch_id, text='Sorry! This room info is not ready.')

        elif query == 'move_status':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Room 1', callback_data='room1_move_status')],
                [InlineKeyboardButton(text='Room 2', callback_data='room2_move_status')],
                [InlineKeyboardButton(text='Room 3', callback_data='room3_move_status')]
            ])
            self.bot.sendMessage(ch_id, text='Which room would you like to check movement status?(Please consider currently Room_1 has been activated)', reply_markup=keyboard)

        elif query in ['room1_move_status', 'room2_move_status', 'room3_move_status']:
            if query == 'room1_move_status':
                url = 'http://127.0.0.1:8081/move-status'
                response = requests.get(url)
                self.bot.sendMessage(ch_id, text=f'Status of movement inside Room 1 is:\n{response.text}')
            else:
                self.bot.sendMessage(ch_id, text='Sorry! This room info is not ready.')

        elif query == 'on':
            url = 'http://127.0.0.1:8081/on'
            response = requests.get(url)
            if response.text == "on":
                self.bot.sendMessage(ch_id, text='Light switched ON successfully!')
            else:
                self.bot.sendMessage(ch_id, text='Failed to switch ON the light.')

        elif query == 'off':
            url = 'http://127.0.0.1:8081/off'
            response = requests.get(url)
            if response.text == "off":
                self.bot.sendMessage(ch_id, text=f'Light switched OFF successfully!')
            else:
                self.bot.sendMessage(ch_id, text='Failed to switch OFF the light.')

        elif query in ['room_1', 'room_2', 'room_3']:
            if query == 'room_1':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Sensor', callback_data='sensor')],
                    [InlineKeyboardButton(text='Actuator', callback_data='actuator')]
                ])
                self.bot.sendMessage(ch_id, text='Which feature would you like to update?', reply_markup=keyboard)
            else:
                self.bot.sendMessage(ch_id, text='Sorry! This room info is not ready.')


# -----------------------------------------------------------------
# Update Catalog
# -----------------------------------------------------------------
        elif query == 'sensor':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='SensorID', callback_data='sensor_id')],
                [InlineKeyboardButton(text='sensorType', callback_data='sensor_type')],
                [InlineKeyboardButton(text='MeasureType', callback_data='measure_type')],
                [InlineKeyboardButton(text='servicesDetails', callback_data='service')]
            ])
            self.bot.sendMessage(ch_id, text='Which feature would you like to update?', reply_markup=keyboard)


        elif query == 'actuator':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Actuator_Type', callback_data='actuator_type')],
                [InlineKeyboardButton(text='Properties', callback_data='properties')]
            ])
            self.bot.sendMessage(ch_id, text='Which feature would you like to update?', reply_markup=keyboard)

        # -----------------------------------------------------------------
        # Update Catalog___check(add/remove)
        # -----------------------------------------------------------------
        elif query == 'sensor_id':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            sensor_id = file['rooms']['room1'][0]['sensor']['sensorId']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_id')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_id')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(sensor_id)} sensorID available:\n'
                                             f'1- {sensor_id[0]}\n'
                                             f'Do you want to add new one or remove current ID?', reply_markup=keyboard)

        elif query == 'sensor_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            sensor_type = file['rooms']['room1'][0]['sensor']['sensorType']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_type')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_type')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(sensor_type)} sensorType available:\n'
                                             f'1- {sensor_type[0]}\n'
                                             f'2-{sensor_type[1]}.\n'
                                             f'Do you want to add new one or remove current sensorTypes?', reply_markup=keyboard)


        elif query == 'measure_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            measure_type = file['rooms']['room1'][0]['sensor']['measureType']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add_MT', callback_data='add_mt')],
                [InlineKeyboardButton(text='Remove_MT', callback_data='remove_mt')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(measure_type)} MeasureType available:\n'
                                             f'1- {measure_type[0]}\n'
                                             f'2-{measure_type[1]}.\n'
                                             f'Do you want to add new one or remove current measureType?', reply_markup=keyboard)

        elif query == 'service':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='serviceType', callback_data='service_type')],
                [InlineKeyboardButton(text='serviceIP', callback_data='service_ip')],
                [InlineKeyboardButton(text='topic', callback_data='topic')]
            ])
            self.bot.sendMessage(ch_id, text='Which feature would you like to update?', reply_markup=keyboard)


        elif query == 'service_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            service_type = file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceType']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_service_type')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_service_type')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(service_type)} serviceType available:\n'
                                             f'1- {service_type[0]}\n'
                                             f'2-{service_type[1]}.\n'
                                             f'Do you want to add new one or remove current serviceTypes?', reply_markup=keyboard)

        elif query == 'service_ip':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            service_ip = file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceIP']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_service_ip')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_service_ip')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(service_ip)} serviceIP available:\n'
                                             f'1- {service_ip[0]}\n'
                                             f'Do you want to add new one or remove current serviceIPs?', reply_markup=keyboard)

        elif query == 'topic':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            topic = file['rooms']['room1'][0]['sensor']['servicesDetails']['topic']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_topic')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_topic')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(topic)} topic available:\n'
                                             f'1- {topic[0]}\n'
                                             f'Do you want to add new one or remove current topic?', reply_markup=keyboard)


        elif query == 'actuator_type':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            actuator_type = file['rooms']['room1'][0]['Actuator']['Actuator_Type']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_actuator_type')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_actuator_type')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(actuator_type)} ActuatorType available:\n'
                                             f'1- {actuator_type[0]}\n'
                                             f'Do you want to add new one or remove ActuatorType?', reply_markup=keyboard)

        elif query == 'properties':
            with open('catalog.json', 'r') as f:
                file = json.load(f)

            properties = file['rooms']['room1'][0]['Actuator']['Properties']['Type']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Add', callback_data='add_properties')],
                [InlineKeyboardButton(text='Remove', callback_data='remove_properties')]
            ])
            self.bot.sendMessage(ch_id, text=f'There are {len(properties)} properties available:\n'
                                             f'1- {properties[0]}\n'
                                             f'Do you want to add new one or remove Properties?', reply_markup=keyboard)



        # -----------------------------------------------------------------
        # Update Catalog___Add section
        # -----------------------------------------------------------------
        elif query == 'add_id':
            self.user_state[ch_id] = 'Waiting_add_id'
            self.bot.sendMessage(ch_id, text='Please write the new sensorID:')

        elif query == 'add_type':
            self.user_state[ch_id] = 'Waiting_add_sensor_type'
            self.bot.sendMessage(ch_id, text='Please write the new sensorType:')

        elif query == 'add_mt':
            self.user_state[ch_id] = 'Waiting_add_measuretype'
            self.bot.sendMessage(ch_id, text='Please write the new MeasureType:')

        elif query == 'add_service_type':
            self.user_state[ch_id] = 'Waiting_add_service_type'
            self.bot.sendMessage(ch_id, text='Please write the new serviceType:')

        elif query == 'add_service_ip':
            self.user_state[ch_id] = 'Waiting_add_service_ip'
            self.bot.sendMessage(ch_id, text='Please write the new serviceIP:')

        elif query == 'add_topic':
            self.user_state[ch_id] = 'Waiting_add_topic'
            self.bot.sendMessage(ch_id, text='Please write the new topic:')

        elif query == 'add_actuator_type':
            self.user_state[ch_id] = 'Waiting_add_actuator_type'
            self.bot.sendMessage(ch_id, text='Please write the new ActuatorType:')

        elif query == 'add_properties':
            self.user_state[ch_id] = 'Waiting_add_actuator_properties'
            self.bot.sendMessage(ch_id, text='Please write the new Properties:')



        # -----------------------------------------------------------------
        # Update Catalog___Remove section
        # -----------------------------------------------------------------

        elif query == 'remove_id':
            self.user_state[ch_id] = 'Waiting_remove_id'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            sensor_id = file['rooms']['room1'][0]['sensor']['sensorId']
            self.bot.sendMessage(ch_id, text=f'Available sensorID:\n'
                                             f'1- {sensor_id[0]}\n'
                                             f'Please write the number.')

        elif query == 'remove_type':
            self.user_state[ch_id] = 'Waiting_remove_remove_type'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            sensor_type = file['rooms']['room1'][0]['sensor']['sensorType']
            self.bot.sendMessage(ch_id, text=f'Available sensorType:\n'
                                             f'1- {sensor_type[0]}\n'
                                             f'2-{sensor_type[1]}.\n'
                                             f'Please write the number.')

        elif query == 'remove_mt':
            self.user_state[ch_id] = 'Waiting_remove_measureType'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            measure_type = file['rooms']['room1'][0]['sensor']['measureType']
            self.bot.sendMessage(ch_id, text=f'Available measureType:\n'
                                             f'1- {measure_type[0]}\n'
                                             f'2-{measure_type[1]}.\n'
                                             f'Please write the number.')

        elif query == 'remove_service_type':
            self.user_state[ch_id] = 'Waiting_remove_service_type'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            service_type = file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceType']
            self.bot.sendMessage(ch_id, text=f'Available serviceType:\n'
                                             f'1- {service_type[0]}\n'
                                             f'2-{service_type[1]}.\n'
                                             f'Please write the number.')

        elif query == 'remove_service_ip':
            self.user_state[ch_id] = 'Waiting_remove_service_ip'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            service_ip = file['rooms']['room1'][0]['sensor']['servicesDetails']['serviceIP']
            self.bot.sendMessage(ch_id, text=f'Available serviceIP:\n'
                                             f'1- {service_ip[0]}\n'
                                             f'Please write the number.')

        elif query == 'remove_topic':
            self.user_state[ch_id] = 'Waiting_remove_topic'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            topic = file['rooms']['room1'][0]['sensor']['servicesDetails']['topic']
            self.bot.sendMessage(ch_id, text=f'Available topic:\n'
                                             f'1- {topic[0]}\n'
                                             f'Please write the number.')

        elif query == 'remove_actuator_type':
            self.user_state[ch_id] = 'Waiting_remove_actuator_type'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            actuator_type = file['rooms']['room1'][0]['Actuator']['Actuator_Type']
            self.bot.sendMessage(ch_id, text=f'Available Actuator_Type:\n'
                                             f'1- {actuator_type[0]}\n'
                                             f'Please write the number.')

        elif query == 'remove_properties':
            self.user_state[ch_id] = 'Waiting_remove_properties'
            with open('catalog.json', 'r') as f:
                file = json.load(f)
            properties = file['rooms']['room1'][0]['Actuator']['Properties']['Type']
            self.bot.sendMessage(ch_id, text=f'Available Properties_Type:\n'
                                             f'1- {properties[0]}\n'
                                             f'Please write the number.')

if __name__ == '__main__':
    bot = MyBOT(token)
    bot.start()
    while True:
        time.sleep(1)


