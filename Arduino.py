import os
import time
import cherrypy
import json
import paho.mqtt.client as PahoMQTT

from notifier import Notifier


class Arduino:
    exposed = True

    def __init__(self, clientID, broker, port, notifier):
        self.lights = False
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID
        self._topic = ""
        self._isSubscriber = False
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, True)  
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
 
 
    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        # A new message is received
        self.notifier.notify (msg.topic, msg.payload)
 
    def myPublish(self, topic, msg):
        # publish a message with a certain topic
        self._paho_mqtt.publish(topic, json.dumps(msg), 2)
        print("[DEBUG] publishing topic %s" % (topic))

    def mySubscribe (self, topic):
        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2) 
        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic
        print ("subscribed to %s" % (topic))
 
    def start(self):
        #manage connection to broker
        self._paho_mqtt.connect(self.broker , self.port)
        self._paho_mqtt.loop_start()

    def unsubscribe(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber 
            self._paho_mqtt.unsubscribe(self._topic)
            
    def stop (self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber 
            self._paho_mqtt.unsubscribe(self._topic)
 
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()
    
    def loop_forever(self):
        self._paho_mqtt.loop_forever()

    ## Arduino Daemon
    def daemon():
        while True:
            time.sleep(1)
        return None

    ## ------------
    
    def GET(self, *uri):
        res = ''
        if uri[0] == "on":
            self.lights = True
            res = "on" if self.lights else "off"
        elif uri[0] == "off":
            self.lights = False
            res = "on" if self.lights else "off"
        elif uri[0] == "status":
            res = "on" if self.lights else "off"
            # TODO add sensors status
        else:
            res = open('index.html')
            #res = open(os.path.abspath(os.path.join("..", "webroot", "index.html")))
            #res = "error"
        return res

    #def PUT(self, *uri):
    #    command = uri[0]
    #    self.led_client.publish(command)
        
if __name__ == '__main__':
    # TO FIX WITH CATALOG.json
    # ----------------------------
    with open("../settings.json") as f:
    	conf = json.load(f)
    roomIDs = ["room%d" % (i+1) for i in range(conf["rooms"])]
    topics = []
    for room in roomIDs:
        for sensor_type in conf["sensors"]:
            topics.append('/'.join([room, str(len(topics)) + '_sensor']))
    #arduino.myPublish("test", {"messaggio":"messaggio di prova"})
    # ------------------------------
    arduino = Arduino("arduino", conf["broker"], int(conf["port"]), Notifier())
    print("[start] starting web server")
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            #'tools.session.on': True,
            'tools.staticdir.root': os.path.abspath(os.path.join("..", "webroot"))
        },
        # You need to include the part below if you want to activate the css and gice to the button a nicer look
        '/dashboard': {
            'tools.staticdir.on': True,
            'tools.staticdir.index': 'index.html',
            'tools.staticdir.dir': os.path.abspath(os.path.join("..", "webroot"))
        }
    }
    cherrypy.config.update({'server.socket_host': "0.0.0.0", 'server.socket_port': 8099})
    cherrypy.tree.mount(arduino, '/', conf)
    cherrypy.engine.start()
    #cherrypy.engine.block()
    print("[start] starting sensors (mqtt)")
    arduino.start()
    for topic in topics:
        arduino.mySubscribe(topic)
    arduino.daemon()
    arduino.stop()
