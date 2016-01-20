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

import unittest

import tests

from pitmaster.tools import sensor
from pitmaster.exceptions import *


class MyTestCase(unittest.TestCase):

    def test_read_temp_sensor(self):
        my_sen = tests.data_dir + "/mock_sensor_file"
        temp = sensor.read_temp(my_sen)
        self.assertEqual(20.0, temp)

    def test_read_temp_raises_exception_when_missing_sensor(self):
        with self.assertRaises(MissingPropertyException):
            sensor.read_temp()

    def test_read_temp_raises_exception_when_sensor_not_found(self):
        with self.assertRaises(SensorNotFoundException):
            sensor.read_temp("/foo/bar")
