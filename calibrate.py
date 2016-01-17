
import os
import sys
import time
import getopt
import lib.common

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


def calibrate_hot(sensor, help=True):
    if help:
        print "The 'hot' calibraiton finds the differenance between what the"
        print "sensor reads and the actual boiling point of water."
        print ""
        print "To do this, bring 3 inches of water to a rolling boil,"
        input("place the sensor in the water, then press enter to calibrate.")
    offset = -1 * (100 - avg_temp(sensor))
    print "Hot offset for " + sensor + "is " + offset + " C"
    return offset


def calibrate_cold(sensor, help=True):
    if help:
        print "The 'cold' calibraiton finds the differenance between what the"
        print "sensor reads and the actual freezing point of water."
        print ""
        print "To do this, fill a tall glass with ice, then cold water. Then,"
        print "wait one minute, and then swirl the sensor in the water."
        input("Press enter when you're ready to calibrate")
    offset = -1 * (100 - avg_temp(sensor))
    print "Cold offset for " + sensor + "is " + offset + " C"
    return offset


def avg_temp(sensor):
    total_temp = None
    for i in range(0, 2):
        raw_temp = read_temp(0, sensor)
        print "Raw tem " + raw_temp + "C Reading " + (i + 1)
        total_temp = total_temp + raw_temp
        time.sleep(2)

    return float(total_temp)


def run_wizard(sensors):
    single_point = raw_input("Single point calibration? [Y/n] ")
    if str(single_point[0]).upper == "Y":
        hot_calibration = raw_input("Hot? [Y/n] ")
        for sensor in sensors:
            if str(hot_calibration[0]).upper == "Y":
                calibrate_hot(sensor)
            else:
                calibrate_cold(sensor)
    else:
        for sensor in sensors:
            calibrate_hot(sensor)
            calibrate_cold(sensor)


def main(argv):
    sensors = enumerate_sensors()
    run_wizard(sensors)

if __name__ == "__main__":
    main(sys.argv[1:])
