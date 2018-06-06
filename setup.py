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

import config
import sqlite3
import os
from contextlib import closing

def init_db():
    with closing(connect_db()) as db:
        with open('db/demo.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(config.config['db_name'])

if __name__ == '__main__':
    try:
        os.remove(config.config['db_name'])
    except: pass
    init_db()
    print("Database %s created"%(config.config['db_name'],))

