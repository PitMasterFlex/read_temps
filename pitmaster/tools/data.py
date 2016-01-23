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

from pitmaster.exceptions import *


class DBObject(object):

    def __init__(self, filename=None):
        """

        :param filename:
        :return:
        """
        self.filename = filename
        self.db = sqlite3.connect(self.filename)
        self.db.row_factory = sqlite3.Row

    def _renew_connection(self):
        self.db = sqlite3.connect(self.filename)

    def save(self, info=None):
        """

        :param info:
        :return:
        """
        if info is None:
            raise MissingPropertyException("info must not be None!")
        conn = self.db.cursor()
        conn.execute("Insert into cook_data_entry VALUES (?,?,?,?,?)", (
            info["date"],
            info["temp_f"],
            info["temp_c"],
            info["probe_name"],
            info["cook_name"]
        ))
        self.db.commit()

    def list_all_by_cook(self, cook_name=None):
        """
        Return all entries in the database for a given cook.

        :param cook_name:
        :return:
        """
        conn = self.db.cursor()
        query = conn.execute("Select * from cook_data_entry where cook_name=?",
                             cook_name)
        info = query.fetchall()
        return info

    def get(self, entry_id=None):
        """
        Return a temp_event entry based on its id.
        :param entry_id:
        :param max_results:
        :return:
        """
        conn = self.db.cursor()
        query = conn.execute("SELECT * from cook_data_entry where id=?", entry_id)
        info = query.fetchone()
        return info
