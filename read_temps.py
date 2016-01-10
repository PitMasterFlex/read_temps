import os, sys, getopt
import time
import csv
from datetime import datetime

# Sensor.
# Need a way to enumerate these, rather than set statically.
sensor_id = '3b-0000001921e8'
temp_sensor = '/sys/bus/w1/devices/' + sensor_id + '/w1_slave'

def usage():
	print "sudo read_temps.py --help --output=[csv, JSON] --cookname=Turkey --datadir=/tmp/sensor_data"

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

def csvwriter(data_file, cook_name, t, temp):
	with open(data_file, 'a', 0) as csvfile:
		writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
		writer.writerow([cook_name, t, temp])

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
			csvwriter(data_file, cook_name, t, temp)
		elif output == "json":
			jsonwriter(data_dir, t, temp)

		time.sleep(1)

# Do the things
if __name__ == "__main__":
	main(sys.argv[1:])