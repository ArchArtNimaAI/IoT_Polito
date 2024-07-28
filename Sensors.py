import random
import json
from Arduino import Arduino
import time

class Sensor():
	"""docstring for Sensor"""
	def __init__(self, roomID, sensorID, broker, port):
		self.roomID = roomID
		self.sensorID = str(sensorID)+'_sensor'
		self.topic = '/'.join([self.roomID, self.sensorID])
		# TODO pensiamo se evitare di utilizzare Arduino come base di codice comune
		self.client = Arduino(self.sensorID, broker, port, None)
		self.__message = {
			'roomID':self.roomID,
			'bn':self.sensorID,
			'e':
				[
					{'n':'movement','value':'', 'timestamp':'','unit':'C'},
					{'n':'illumination','value':'', 'timestamp':'','unit':'%'}
				]
			}
		self.illumination_data = None
		with open("../scripts/light.csv", 'r') as f:
			self.illumination_data = f.readlines()[1:]
		self.seconds = 0
		self.lastrow = 0
		print(self.illumination_data)

	def sendData(self):
		message=self.__message
		#message['e'][0]['value']=random.randint(10,30)
		#message['e'][1]['value']=random.randint(50,90)
		message['e'][0]['timestamp']=str(time.time())
		message['e'][1]['timestamp']=str(time.time())
		self.client.myPublish(self.topic,message)
	
	def sendDataMovement(self):
		message=self.__message
		message['e'][0]['value'] = (random.randint(0,1) == 1)
		self.sendData()
	
	def sendDataIllumination(self):
		if self.seconds == 0:
			message = self.__message
			message['e'][1]['value'] = int(self.illumination_data[self.lastrow].split(',')[1]) #random.randint(50,90)
			self.sendData()
			self.lastrow = (self.lastrow + 1) % (len(self.movement_data))
		self.seconds = (self.seconds + 1) % 1

	def start (self):
		self.client.start()

	def stop (self):
		self.client.stop()

if __name__ == '__main__':
	with open("../settings.json") as f:
		conf = json.load(f)
	roomIDs = ["room%d" % (i+1) for i in range(conf["rooms"])]
	broker=conf["broker"]
	port=conf["port"]
	Sensors = []
	for room in roomIDs:
		for sensor_type in conf["sensors"]:
			if sensor_type == "movement":
				sensor = Sensor(room, len(Sensors), broker, port)
				Sensors.append(sensor)
			elif sensor_type == "illumination":
				sensor = Sensor(room, len(Sensors), broker, port)
				Sensors.append(sensor)
	for sensor in Sensors:
		sensor.start()
	while True:
		for sensor in Sensors:
			sensor.sendDataMovement()
			sensor.sendDataIllumination()
		time.sleep(1)
