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
from numbers import Number

from pitmaster.exceptions import *


def from_c_to_f(temp=None):
    """
    Converts a given temp from Celsius to fahrenheit

    :param temp:
    :return:
    """
    if temp is None:
        raise MissingPropertyException("temp can not be None!")
    if not isinstance(temp, Number):
        raise InvalidPropertyException(
            "temp must be a valid number. Found: {}".format(type(temp))
        )
    return (temp * 9/5) + 32.0
