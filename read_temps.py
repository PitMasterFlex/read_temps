
import os
import sys
import getopt
import time
import csv
import json
from datetime import datetime
import pygame

# Sensor.
# Need a way to enumerate these, rather than set statically.
SENSOR_ID = '3b-0000001921e8'
TEMP_SENSOR = '/sys/bus/w1/devices/' + SENSOR_ID + '/w1_slave'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

def usage():
    print "sudo read_temps.py --help --output=[csv, JSON] --cookname=Turkey"
    print "--datadir=/tmp/sensor_data"
    print ""
    print " --help      print this help."
    print " --output    Set output type as CSV or JSON. CSV is default."
    print " --cookname  User friendly name for this cooking session. Defaults to current date."
    print " --datadir   Where to store the data collected."
    print " --verbose   Display temp readings on console."


def temp_raw():
    file_reader = open(TEMP_SENSOR, 'r')
    lines = file_reader.readlines()
    file_reader.close()
    return lines


def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3] != 'Y':
        print lines[0].strip()[-3]
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def csvwriter(data_file, cook_name, epoch_time, sensor_id, temp):
    with open(data_file, 'a', 0) as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([cook_name, sensor_id, epoch_time, temp])


def jsonwriter(data_file, cook_name, epoch_time, sensor_id, temp):
    temp_data = {
        "sensor": sensor_id,
        "time": epoch_time,
        "temp": temp
    }

    if not os.path.isfile(data_file):
        with open(data_file, 'wb', 0) as first_write:
            header_data = {
                "cook": cook_name,
                "startTime": epoch_time,
                "data": [],
            }
            json.dump(header_data, first_write)

    with open(data_file, 'r+', 0) as json_file:
        data = json.load(json_file)
        data['data'].append(temp_data)
        json_file.seek(0)
        json_file.write(json.dumps(data))
        json_file.truncate()


def tft_writer(temp_c):
    os.putenv('SDL_FBDEV', '/dev/fb1')
    pygame.init()
    pygame.mouse.set_visible(False)
    lcd = pygame.display.set_mode((320, 240))
    lcd.fill((0, 0, 0))
    pygame.display.update()
    background = pygame.Surface(lcd.get_size())
    background = background.convert()
    background.fill(WHITE)
    box = pygame.draw.rect(background, YELLOW, (40, 0, 40, 240))
    box = pygame.draw.rect(background, CYAN, (80, 0, 40, 240))
    box = pygame.draw.rect(background, GREEN, (120, 0, 40, 240))
    box = pygame.draw.rect(background, MAGENTA, (160, 0, 40, 240))
    box = pygame.draw.rect(background, RED, (200, 0, 40, 240))
    box = pygame.draw.rect(background, BLUE, (240, 0, 40, 240))
    box = pygame.draw.rect(background, BLACK, (280, 0, 40, 240))
    font_big = pygame.font.Font(None, 60)
    temp = temp_c * 9.0 / 5.0 + 32.0
    lcd.fill((0, 0, 0))
    text_surface = font_big.render('Temp: ' + str(temp) + "F", True, WHITE)
    rect = text_surface.get_rect(center=(160, 120))
    lcd.blit(text_surface, rect)
    pygame.display.update()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ho:c:d:vt", ["help", "output=", "cookname=", "datadir=", "verbose", "tft"])
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
        else:
            assert False, "unhandled option"

    # init the 1-wire interface
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # Set or variables
    data_dir = data_dir or '/home/pi/projects/read_temps/data/'
    output = output or "csv"

    datestring = datetime.now()
    date_time = datestring.strftime('%m%d%Y')
    cook_name = cook_name or date_time

    while True:
        temp = read_temp()
        epoch_time = str(time.time())
        if tft:
            tft_writer(temp)
        if verbose:
            print str(epoch_time) + ", " + str(temp)
        if output == "csv":
            data_file = data_dir + cook_name + ".csv"
            csvwriter(data_file, cook_name, epoch_time, SENSOR_ID, temp)
        elif output == "json":
            data_file = data_dir + cook_name + ".json"
            jsonwriter(data_file, cook_name, epoch_time, SENSOR_ID, temp)
        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])
