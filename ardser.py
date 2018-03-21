import serial
import time
import requests
import json, struct
from time import sleep

command = 10
token = "Bearer Ulswzb9BnQnqzIc8rad2ggtt"
api_url = "https://air.kiisu.club/v1/data"

ser = serial.Serial(
	port = '/dev/ttyACM0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	timeout = 1
)

def sendData(data):
	try:
		send_data = json.dumps({"datum": {"device_id": data['Device_ID'], "temperature": data['Temperature'], "humidity": data['Humidity']}})
		header = {'Authorization':token,'Content-type': 'application/json'}
		req = requests.post(api_url, data=send_data, headers=header)
	except requests.exceptions.RequestException as e:
		return e
	if req.status_code == 201:
		return "Data sent " + str(req.status_code)
	else:
		return "Error: " + str(req.status_code)



ser.flushInput()

while True:
	ser.write(struct.pack('>B', command))
	linein = ser.readline().strip()
	if linein:
		values = linein.split()
		print linein
		if len(values) > 2:
			values = [values[n:n+2] for n in range(0, len(values), 2)]
			keyr = dict(values)
			print sendData(keyr)
		linein = ""
		sleep(10)
