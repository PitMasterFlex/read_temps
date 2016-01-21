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

import argparse
import sys

from pitmaster.tools.display import LocalDisplay
from pitmaster.tools import temps
from pitmaster.tools import sensor


def _setup_arg_parser():
    parser = argparse.ArgumentParser(
        description='Standard arguments for read_temps'
    )

    parser.add_argument(
        '-d',
        '--datadir',
        required=True,
        action='store',
        help="Full path on file system where data is stored."
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        action='store',
        help="Full path on file system where output is stored"
    )
    parser.add_argument(
        "-c",
        "--cookname",
        required=False,
        action='store',
        help="Friendly name to give your cook. Default is a time stamp."
    )
    parser.add_argument(
        "-t",
        "--tft",
        action='store_true',
        help="Enable the LCD display or not. It is disabled by default."
    )
    return parser


def execute():
    """
    Executable
    :return:
    """
    parser = _setup_arg_parser()
    provided_args = parser.parse_args(sys.argv[1:])
    data_dir = provided_args.datadir
    cook_name = provided_args.cookname
    output_file = provided_args.output
    use_lcd = provided_args.tft
    sensors = sensor.find_temp_sensors()
    if use_lcd:
        display = LocalDisplay()
        display.set_display_msg("Welcome!")
    while True:
        for sen in sensors:
            temp_c = sensor.read_temp(sen["location"])
            temp_f = temps.from_c_to_f(temp=temp_c)
            if use_lcd:
                display.check_events()
                display.set_display_msg("{}: {}".format(
                    sen["name"],
                    temp_f
                ))


if __name__ == "__main__":
    execute()
