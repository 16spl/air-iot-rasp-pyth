import serial
import time
import requests
import json, struct, os, serial.tools.list_ports
from time import sleep

command = 'a'
send_interval = 60 										#In seconds
token_file = os.path.expanduser("~/.rasp-pyth-token") 	#Token is read from user's home
api_url = "https://air.kiisu.club/v1/data" 				#Api endpoint

with open(token_file) as f:
	token = f.readlines()

ser = serial.Serial(
	port = '/dev/ttyACM0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	timeout = 1
)
ser.setDTR(False)
sleep(0.022)
ser.setDTR(True)
ser.flushInput()

def sendData(data):
	try:
		send_data = json.dumps({"datum": {
								"device_id": data['Device_ID'],
								"temperature": data['Temperature'],
								"humidity": data['Humidity'],
								"co2": data['CO2']
								}})
		header = {'Authorization':token[0].rstrip(),'Content-type': 'application/json'}
		req = requests.post(api_url, data=send_data, headers=header)
	except requests.exceptions.RequestException as e:
		return e
	if req.status_code == 201:
		return "Data sent " + str(req.status_code)
	else:
		return "Error: " + str(req.status_code)

print "Data sending interval: " + str(send_interval) + " seconds"
print "Waiting for arduino..."

while True:
	linein = ser.readline().strip()
	print linein
	if linein == 'Done':
		linein = ""
		break
	linein = ""

while True:
	ser.write(command)
	linein = ser.readline().strip()
	if linein:
		values = linein.split()
		print linein
		if len(values) > 2:
			values = [values[n:n+2] for n in range(0, len(values), 2)]
			keyr = dict(values)
			print sendData(keyr)
		linein = ""
		sleep(send_interval)
