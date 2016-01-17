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

from pitmaster.tools import temps
from pitmaster.exceptions import *


class TestPitmasterToolsTemps(unittest.TestCase):

    def test_c_to_f_when_c_0(self):
        c_temp = 0
        expected = 32
        actual = temps.from_c_to_f(c_temp)
        self.assertEqual(expected, actual)

    def test_c_to_f_when_c_negative(self):
        c_temp = -11.2
        expected = 11.84
        actual = temps.from_c_to_f(c_temp)
        self.assertEqual(expected, actual)

    def test_c_to_f_when_c_positive(self):
        c_temp = 107.6
        expected = 225.68
        actual = temps.from_c_to_f(c_temp)
        self.assertEqual(expected, actual)

    def test_c_to_f_when_c_none_raises_missing_property(self):
        c_temp = None
        with self.assertRaises(MissingPropertyException) as c:
            temps.from_c_to_f(c_temp)
        self.assertEqual("temp can not be None!", c.exception.message)

    def test_c_to_f_when_c_str_invalid_prop_exception_raised(self):
        c_temp = "hello"
        with self.assertRaises(InvalidPropertyException) as c:
            temps.from_c_to_f(c_temp)
        self.assertIn("temp must be a valid number", c.exception.message)
