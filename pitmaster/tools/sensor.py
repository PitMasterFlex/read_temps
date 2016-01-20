#   Copyright 2016 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import time

from pitmaster.exceptions import *


def _temp_raw(sensor=None):
    with open(sensor, "r") as file_reader:
        lines = file_reader.readlines()
    return lines


def read_temp(sensor=None, offset=None):
    """
    Reads the temp sensor and returns its temp in C.

    :param sensor: Full path to the sensor file to read from
    :param offset: Offset in degrees C from a standard reference
    :return: Temp in C
    """
    if sensor is None:
        raise MissingPropertyException("sensor must not be None!")
    if offset is None:
        offset = 0
    if not os.path.isfile(sensor):
        raise SensorNotFoundException("Unable to locate: {}".format(sensor))
    lines = _temp_raw(sensor)
    while lines[0].strip()[-3] != 'Y':
        time.sleep(0.2)
        lines = _temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = (float(temp_string) / 1000.0) + offset
        return temp_c


if __name__ == "__main__":
    for i in range(15):
        test = read_temp(sensor="/sys/bus/w1/devices/3b-0000001921e8/w1_slave")
        print test
