import random
import time
import requests

for i in range (10):
    data = random.randint(1,34)
    requests.get( 'https://api.thingspeak.com/update?api_key=D3SC36XQ0FKQEAZC&field1=%s'%data)
    time.sleep((20))
