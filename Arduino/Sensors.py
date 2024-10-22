import random
import json
import os
from arduino import Arduino
import time

class Sensor():
    """docstring for Sensor"""
    def __init__(self, sensorID, broker, port):
        self.sensorID = sensorID
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
        self.illumination_data = None
        with open("..\lightFiles\light.csv", 'r') as f:
            self.illumination_data = f.readlines()[1:]
        self.seconds = 0
        self.lastrow = 0

    def sendData(self):
        self.message = self.__message
        # message['e'][0]['value']=random.randint(10,30)
        # message['e'][1]['value']=random.randint(50,90)
        self.message['e'][0]['timestamp'] = str(time.time())
        self.message['e'][1]['timestamp'] = str(time.time())
        self.client.myPublish(self.topic, self.message)

    def setDataMovement(self):
        self.message = self.__message
        self.message['e'][0]['value'] = (random.randint(0, 1) == 1)

    def setDataIllumination(self):
        if self.seconds == 0:
            self.message = self.__message
            self.message['e'][1]['value'] = int(self.illumination_data[self.lastrow].split(',')[1])  # random.randint(50,90)
            self.lastrow = (self.lastrow + 1) % (len(self.illumination_data))
        self.seconds = (self.seconds + 1) % 60

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()


if __name__ == '__main__':
    with open("..\settings.json") as f:
        conf = json.load(f)
    broker = conf["broker"]
    port = conf["port"]
    sensor = Sensor("sensor", broker, port)
    sensor.start()
    while True:
        print("seconds: " + str(sensor.seconds))

        sensor.setDataMovement()
        sensor.setDataIllumination()
        sensor.sendData()
        time.sleep(1)

