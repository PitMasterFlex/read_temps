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
import time

from pitmaster.tools.display import LocalDisplay
from pitmaster.tools import temps
from pitmaster.tools import sensor
from pitmaster.tools.data import DBObject


def _setup_arg_parser():
    parser = argparse.ArgumentParser(
        description='Standard arguments for read_temps'
    )

    parser.add_argument(
        '-d',
        '--datadir',
        required=False,
        action='store',
        help="Full path on file system where data is stored."
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        action='store',
        help="Full path on file system where output is stored. "
             "This should be a directory, and should already exist."
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
    output_file = "/home/pi/pitmaster_flex.sq3"
    use_lcd = provided_args.tft
    sensors = sensor.find_temp_sensors()
    data_obj = DBObject(filename=output_file)
    if use_lcd:
        display = LocalDisplay()
        display.set_display_msg("Welcome!")
    try:
        while True:
            for sen in sensors:
                temp_c = sensor.read_temp(sen["location"])
                temp_f = temps.from_c_to_f(temp=temp_c)
                info = {
                    "date": time.time(),
                    "temp_f": temp_f,
                    "temp_c": temp_c,
                    "probe_name": sen["name"],
                    "cook_name": cook_name
                }
                data_obj.save(info=info)
                if use_lcd:
                    display.check_events()
                    display.set_display_msg("{}: {}f".format(
                        sen["name"],
                        temp_f
                    ))
                time.sleep(3)
    except KeyboardInterrupt:
        print
        for i in data_obj.list_all_by_cook(cook_name=cook_name):
            print i
        raise SystemExit


if __name__ == "__main__":
    execute()
