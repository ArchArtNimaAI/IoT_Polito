import os
import time
import cherrypy
import json
import paho.mqtt.client as PahoMQTT
from datetime import datetime
import requests
from notifier import Notifier

class Arduino:
    exposed = True

    def __init__(self, clientID, broker, port, notifier):
        self.lights = False
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID
        self.lastmove = int(time.time())
        self.threshold = 500
        self.timeout = 5 # 30*60
        self._topic = ""
        self._isSubscriber = False
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    # ACTION => MAKE CHANGES
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        self.notifier.notify(msg.topic, msg.payload)
        print(msg.topic)
        print(msg.payload)
        # check movement
        if msg.topic == "magicsensor":
            events = json.loads(msg.payload.decode())["e"]
            light = [x for x in events if x["n"] == "illumination"][0]["value"]  # ["n"]["illumination"]["value"]
            movement = [x for x in events if x["n"] == "movement"][0]["value"]
            print("Raw Payload Received:", msg.payload)

            # movement = e["n"]["movement"]["value"]
            print("[DEBUG] light: " + str(light))
            print("[DEBUG] move: " + str(movement))
            if movement == True and light < self.threshold:
                self.lastmove = int(time.time())
                if self.lights == False:
                    self.lights = True
                    self.myPublish("actuator", {"action": "lights on"})

###--------- Comunication with ThinkSpeak----------------------------------------------

            movement_numeric = None
            if movement:
                movement_numeric = 1
            else:
                movement_numeric = 0
            requests.get(f'https://api.thingspeak.com/update?api_key=EQ9RQD25DPHUGM3L&field1={light}&field2={movement_numeric}')

###--------- Comunication with ThinkSpeak----------------------------------------------

    def myPublish(self, topic, msg):
        # publish a message with a certain topic
        self._paho_mqtt.publish(topic, json.dumps(msg), 2)

    def mySubscribe(self, topic):
        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2)
        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic
        print("subscribed to %s" % (topic))

    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()

    def unsubscribe(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

    def stop(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def loop_forever(self):
        self._paho_mqtt.loop_forever()

    ## Arduino Daemon
    def daemon(self):
        while True:
            now = datetime.fromtimestamp(int(time.time()))
            last = datetime.fromtimestamp(self.lastmove)
            if ((now - last).total_seconds() > self.timeout):
                self.lights = False
                self.myPublish("actuator", {"action": "lights off"})
            time.sleep(1)
        return None

    ## ------------

    def GET(self, *uri):
        res = ''
        if uri[0] == "on":
            self.lights = True
            self.lastmove = int(time.time())
            self.myPublish("actuator", {"action": "lights on"})
            res = "on" if self.lights else "off"

        elif uri[0] == "off":
            self.lights = False
            self.myPublish("actuator", {"action": "lights off"})
            res = "on" if self.lights else "off"
        elif uri[0] == "light-status":
            res = "on" if self.lights else "off"
        elif uri[0] == "move-status":
            res = str(datetime.fromtimestamp(self.lastmove).strftime('%Y-%m-%d %H:%M:%S'))
        else:
            res = open('index.html')
            # res = open(os.path.abspath(os.path.join("..", "webroot", "index.html")))
            # res = "error"
        return res

    # def PUT(self, *uri):
    #    command = uri[0]
    #    self.led_client.publish(command)


if __name__ == '__main__':
    # TO FIX WITH CATALOG.json
    # ----------------------------
    with open('settings.json') as f:  # ../settings.json or ..\settings.json on windows
        conf = json.load(f)
    topic = "magicsensor"
    # arduino.myPublish("test", {"messaggio":"messaggio di prova"})
    # ------------------------------
    arduino = Arduino("arduino", conf["broker"], int(conf["port"]), Notifier())
    print("[start] starting web server")
    print("[start] starting sensors (mqtt)")
    arduino.start()
    arduino.mySubscribe(topic)
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            # 'tools.session.on': True,
            'tools.staticdir.root': os.path.abspath(os.path.join("..", "webroot"))
        },
        # You need to include the part below if you want to activate the css and gice to the button a nicer look
        '/dashboard': {
            'tools.staticdir.on': True,
            'tools.staticdir.index': 'index.html',
            'tools.staticdir.dir': os.path.abspath(os.path.join("..", "webroot"))
        }
    }
    cherrypy.config.update({'server.socket_host': "0.0.0.0", 'server.socket_port': 8081})
    cherrypy.tree.mount(arduino, '/', conf)
    cherrypy.engine.start()
    # cherrypy.engine.block()

    arduino.daemon()
    arduino.stop()

