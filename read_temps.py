import os, sys, getopt
import time
import csv
from datetime import datetime

# init the 1-wire interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

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

def usage():
	print "sudo read_temps.py --output [csv, JSON] --datadir /tmp/sensor_data"

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
	except getopt.GetoptError as err:
		# print some help thing?
		print(err)
		usage()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o in ("-v", "--verbose"):
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-d", "--datadir"):
			data_dir = a
		else:
			assert False, "unhandled option"

if !data_dir = '/home/pi/projects/read_temps/data/'
sensor_id = '3b-0000001921e8'
temp_sensor='/sys/bus/w1/devices/' + sensor_id + '/w1_slave'


	# Set us up a file to write to.
	d = datetime.now()
	date_time = d.strftime('%m%d%Y')
	data_file = data_dir + date_time + ".csv"

	with open(data_file, 'wb', 0) as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
		while True:
			t = datetime.now().ctime()
			temp = read_temp()
			print(t)
			print(temp)
			# Write our bits out to a CSV, flush it to a file, then sleep.
			csvwriter.writerow([t, temp])
			time.sleep(1)

