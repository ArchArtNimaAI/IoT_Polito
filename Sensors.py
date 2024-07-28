import random
import json
import os
from arduino_final import Arduino
import time
from datetime import datetime

class Sensor():
    """docstring for Sensor"""
    def __init__(self, sensorID, broker, port):
        self.sensorID = "magicsensor"
        self.topic = self.sensorID
        self.message = None
        self.client = Arduino(self.sensorID, broker, port, None)
        self.__message = {
            'bn': self.sensorID,
            'e':
                [
                    {'n': 'movement', 'value': '', 'timestamp': '', 'unit': 'Bool'},
                    {'n': 'illumination', 'value': '', 'timestamp': '', 'unit': 'Lux'}
                ]
        }
        self.movement_data = None
        with open('light.csv', 'r') as f:
            self.movement_data = f.readlines()[1:]
        self.seconds = 0
        self.lastrow = 0

    def sendData(self):
        self.message = self.__message
        timestamp_float = float(time.time())
        actual_date = datetime.fromtimestamp(timestamp_float).strftime('%Y-%m-%d %H:%M:%S')
        self.message['e'][0]['timestamp'] = actual_date #str(time.time())
        self.message['e'][1]['timestamp'] = actual_date #str(time.time())
        self.client.myPublish(self.topic, self.message)

    def setDataMovement(self):
        self.message = self.__message
        self.message['e'][0]['value'] = (random.randint(0, 1) == 1)

    def setDataIllumination(self):
        if self.seconds == 0:
            self.message = self.__message
            self.message['e'][1]['value'] = int(self.movement_data[self.lastrow].split(',')[1])  # random.randint(50,90)
            self.lastrow = (self.lastrow + 1) % (len(self.movement_data))
        self.seconds = (self.seconds + 1) % 5

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()


if __name__ == '__main__':
    with open('settings.json') as f:
        conf = json.load(f)
    broker = conf["broker"]
    port = conf["port"]
    sensor = Sensor("magicsensor", broker, port)
    sensor.start()
    while True:
        print("seconds: " + str(sensor.seconds))
        sensor.setDataMovement()
        sensor.setDataIllumination()
        sensor.sendData()
        time.sleep(1)

