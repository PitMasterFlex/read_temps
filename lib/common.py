
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)


def temp_raw(temp_sensor):
    file_reader = open(temp_sensor, 'r')
    lines = file_reader.readlines()
    file_reader.close()
    return lines


def read_temp(offset, sensor):
    temp_sensor = '/sys/bus/w1/devices/' + sensor + '/w1_slave'
    lines = temp_raw(temp_sensor)
    while lines[0].strip()[-3] != 'Y':
        print lines[0].strip()[-3]
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = (float(temp_string) / 1000.0) + offset
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


def tft_writer(sensor, temp_c):
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
    text_surface = font_big.render('sensor: ' + sensor + 'Temp: ' + str(temp) + "F", True, WHITE)
    rect = text_surface.get_rect(center=(160, 120))
    lcd.blit(text_surface, rect)
    pygame.display.update()


def enumerate_sensors():
    # Sensor.
    # Need a way to enumerate these, rather than set statically.
    # Until then, return the one we have
    sensor_id = '3b-0000001921e8'
    return sensor_id
