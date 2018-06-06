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
    # Database connection
    # mysqli = mysqli_init()
    # mysqli.options(MYSQLI_OPT_CONNECT_TIMEOUT, 5)
    # mysqli.real_connect(config['db_host'],config['db_user'],config['db_password'],config['db_name'])

    try:
        ret = "error"
        con = sqlite3.connect(config.config['db_name'])

        # Get all parameters provided by the javascript
        colname = BeautifulSoup(_POST['colname'], "lxml").get_text()
        id = BeautifulSoup(_POST['id'], "lxml").get_text()
        coltype = BeautifulSoup(_POST['coltype'], "lxml").get_text()
        value = BeautifulSoup(_POST['newvalue'], "lxml").get_text()
        tablename = BeautifulSoup(_POST['tablename'], "lxml").get_text()

        # Here, this is a little tips to manage date format before update the table
        if (coltype == 'date') :
            if (value == "") :
                value = None
            elif '/' in value:
                date = datetime.datetime.strptime(value, '%d/%m/%Y')
                value = date.strftime('%Y-%m-%d')

        cur = con.execute("UPDATE " + tablename + " SET " + colname + " = ? WHERE id = ?", (value, id))
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


