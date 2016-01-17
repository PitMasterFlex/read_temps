
import os
import sys
import time
import getopt
import lib.commonmak

def usage():
    print "sudo read_temps.py --help --one-point=[hot/cold] --two-point \\"
    print "--cookname=Turkey --datadir=/tmp/sensor_data --offset=+20"
    print ""
    print " --help      print this help."
    print " --output    Set output type as CSV or JSON. CSV is default."
    print " --cookname  User friendly name for this cooking session. Defaults to current date."
    print " --datadir   Where to store the data collected."
    print " --offset    Offset in degrees C from a standard reference"
    print " --verbose   Display temp readings on console."


def calibrate_hot(sensor):
    pass

def calibrate_cold(sensor):
    pass


def avg_temp(sensor):
    total_temp = None
    for i in range(0,2):
        total_temp = floattotal_temp + read_temp(0,sensor)
        time.sleep(2)

    return float(total_temp)


def run_wizard():
    single_point = raw_input("Single point calibration? [Y/n] ")
    if str(single_point[0]).upper == "Y":
        hot_calibration = raw_input("Hot? [Y/n] ")
        if str(hot_calibration[0]).upper == "Y":
            sensors = enumerate_sensors()


def main(argv):
    pass
    try:
        opts, args = getopt.getopt(argv, "hot:c:d:vts", ["help", "one-point=", "two-point", "datadir=", "verbose", "tft", "offset="])
    except getopt.GetoptError as err:
        # print some help thing?
        print err
        usage()
        sys.exit(2)

    output = None
    data_dir = None
    cook_name = None
    verbose = False
    tft = False
    offset = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-c", "--cookname"):
            cook_name = arg
        elif opt in ("-d", "--datadir"):
            data_dir = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-t", "--tft"):
            tft = True
        elif opt in ("-s", "--offset"):
            offset = arg
        else:
            assert False, "unhandled option"

