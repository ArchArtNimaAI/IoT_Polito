from arduino_final import Arduino
from notifier import Notifier
import paho.mqtt.client as PahoMQTT
import json
import time
import os

class Actuator(Arduino):
    def __init__(self, clientID, broker, port, notifier):
        self.lights = False
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID
        self._isSubscriber = True
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
    
    # ACTION => MAKE CHANGES
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        self.notifier.notify(msg.topic, msg.payload)
        if msg.topic == "actuator":
            print("[+] Actuator action: " + msg.payload.decode())


if __name__ == '__main__':
    # TO FIX WITH CATALOG.json
    # ----------------------------
    with open('settings.json') as f:  # ../settings.json or ..\settings.json on windows
        conf = json.load(f)
    topic = "actuator"
    actuator = Actuator("actuator", conf["broker"], int(conf["port"]), Notifier())
    print("[start] starting web server")
    print("[start] starting sensors (mqtt)")
    actuator.start()
    actuator.mySubscribe(topic)
    while True:
        time.sleep(1)
    actuator.stop()    
