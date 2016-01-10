import os
import time
import json
from datetime import datetime

data_dir = "/home/pi/projects/read_temps/data/"

# init the 1-wire interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# This is our sensor.
# [todo] figure out how to enumerate this automagically
temp_sensor='/sys/bus/w1/devices/3b-0000001921e8/w1_slave'

# Get the raw temp from the probe
def temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close
	return lines

# Make sure the reading is good
def read_temp():
	lines = temp_raw()
	while lines[0].strip()[-3] != 'Y':
		print(lines[0].strip()[-3])
		time.sleep(0.2)
		lines = temp_raw()
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c

# Set us up a file to write to.
d = datetime.now()
date_time = d.strftime('%m%d%Y')
data_file = data_dir + date_time + ".csv"

with open(data_file, 'wb', 0) as datafile:
	while True:
		t = {
			'probe': '3b-0000001921e8',
			'time': time.mktime(datetime.now().timetuple()),
			'temp': read_temp(),
		}
		json.dump(t, datafile)
		time.sleep(1)