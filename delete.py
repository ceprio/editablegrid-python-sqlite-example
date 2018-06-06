#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#
#   This file is base on EditableGrid example.
#   http://editablegrid.net
#
#   Copyright 2018 by ceprio
#   This file is part of editablegrid-python-sqlite-example which is released under the MIT License.
#   See file LICENCE_1 or go to https://github.com/ceprio/editablegrid-python-sqlite-example for 
#   full license details.

# This script loads data from the database and returns it to the js

import config
import sqlite3
from bs4 import BeautifulSoup
import datetime

def main(_POST):
    try:
        ret = "error"
        con = sqlite3.connect(config['db_name'])

        # Get all parameters provided by the javascript
        id = BeautifulSoup(_POST['id'], "lxml").get_text()
        tablename = BeautifulSoup(_POST['tablename'], "lxml").get_text()

        cur = con.execute("DELETE FROM " + tablename + "  WHERE id = ?", (id,))
        data = cur.fetchall()
        if not data:
            con.commit()
            ret = "ok"
#     except sqlite3.Error as e:
#         self.log.error("Database error: %s" % e)
#     except Exception as e:
#         self.log.error("Exception in _query: %s" % e)
    finally:
        if con:
            con.close()
    return ret

if __name__ == "__main__":
    print(main({'name' : 'Pronovsot', 'firstname' : 'Christian', 'tablename': 'demo'}))


