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

import sqlite3


DB_FILE = "/home/pi/pitmaster_flex.sq3"

db = sqlite3.connect(DB_FILE)

cursor = db.cursor()

query = """
CREATE TABLE "cook_data_entry" (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    `date`  TEXT,
    `temp_f`    INTEGER,
    `temp_c`    INTEGER,
    `probe_name`    TEXT,
    `cook_name` TEXT
)
"""

cursor.execute(query)
db.commit()
db.close()
print "created {}".format(DB_FILE)
