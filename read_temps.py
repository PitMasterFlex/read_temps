import os, sys, getopt
import time
import csv, json
from datetime import datetime

# Sensor.
# Need a way to enumerate these, rather than set statically.
sensor_id = '3b-0000001921e8'
temp_sensor = '/sys/bus/w1/devices/' + sensor_id + '/w1_slave'

def usage():
	print "sudo read_temps.py --help --output=[csv, JSON] --cookname=Turkey --datadir=/tmp/sensor_data"
	print ""
	print "	--help		print this help."
	print " --output 	Set output type as CSV or JSON. CSV is default."
	print " --cookname 	User friendly name for this cooking session. Defaults to current date."
	print " --datadir 	Where to store the data collected."
	print " --display 	Display temp readings on the rPI TFT. Requires CSV."

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

def csvwriter(data_file, cook_name, t, sensor_id, temp):
	with open(data_file, 'a', 0) as csvfile:
		writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
		writer.writerow([cook_name, sensor_id, t, temp])

def jsonwriter(data_file, cook_name, t, sensor_id, temp):
	temp_data = {
		"sensor": sensor_id,
		"time": t,
		"temp": temp
	}
	
	if os.path.isfile(data_file) != True:
		with open(data_file, 'wb', 0) as first_write:
			header_data = {
				"cook": cook_name,
				"startTime": t,
				"data": [],
			}
			json.dump(header_data, first_write)
	
	with open(data_file, 'r+', 0) as file:
		data = json.load(file)
		data['data'].append(temp_data)
		file.seek(0)
		file.write(json.dumps(data))
		file.truncate

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "ho:c:d:c:", ["help", "output=", "cookname=","datadir="])
	except getopt.GetoptError as err:
		# print some help thing?
		print(err)
		usage()
		sys.exit(2)
	
	#Init some of the things
	output = None
	data_dir = None
	verbose = False
	cook_name = None
	
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-c", "--cookname"):
			cook_name = a
		elif o in ("-d", "--datadir"):
			data_dir = a
		else:
			assert False, "unhandled option"

	# init the 1-wire interface
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')

	# Set or variables
	data_dir = data_dir or '/home/pi/projects/read_temps/data/'
	output = output or "csv"

	d = datetime.now()
	date_time = d.strftime('%m%d%Y')
	cook_name = cook_name or date_time

	# Main temp read loop
	while True:
		temp = read_temp()
		t = str(time.time())
		print(t)
		print(temp)
		# Write our bits out, then sleep.
		if output == "csv":
			data_file = data_dir + cook_name + ".csv"
			csvwriter(data_file, cook_name, t, sensor_id, temp)
		elif output == "json":
			data_file = data_dir + cook_name + ".json"
			jsonwriter(data_file, cook_name, t, sensor_id, temp)

		time.sleep(1)

# Do the things
if __name__ == "__main__":
	main(sys.argv[1:])