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
import EditableGrid
from math import ceil

#  ##
#  # fetch_pairs is a simple method that transforms a mysqli_result object in an array.
#  # It will be used to generate possible values for some columns.
#
def fetch_pairs(mysqli, query):
    c = mysqli.execute(query)
    rows = {}
    for row in c.fetchall() :
        value = row[1]
        rows[row[0]] = value
    if len(rows) == 0:
        return None
    return rows

def main(_GET):
    mysqli = sqlite3.connect(config.config['db_name'])

    # create a new EditableGrid object
    grid = EditableGrid.EditableGrid()

    #
    #  Add columns. The first argument of addColumn is the name of the field in the databse.
    #  The second argument is the label that will be displayed in the header

    grid.addColumn('id', 'ID', 'integer', None, False)
    grid.addColumn('name', 'Name', 'string')
    grid.addColumn('firstname', 'Firstname', 'string')
    grid.addColumn('age', 'Age', 'integer')
    grid.addColumn('height', 'Height', 'float')
     # The column id_country and id_continent will show a list of all available countries and continents. So, we select all rows from the tables
    grid.addColumn('id_continent', 'Continent', 'string' , fetch_pairs(mysqli, 'SELECT id, name FROM continent'), True)
    grid.addColumn('id_country', 'Country', 'string', fetch_pairs(mysqli, 'SELECT id, name FROM country'), True)
    grid.addColumn('email', 'Email', 'email')
    grid.addColumn('freelance', 'Freelance', 'boolean')
    grid.addColumn('lastvisit', 'Lastvisit', 'date')
    grid.addColumn('website', 'Website', 'string')
    grid.addColumn('action', 'Action', 'html', None, False, 'id')

    if 'db_tablename' in _GET:
        mydb_tablename = _GET['db_tablename']
    else:
        mydb_tablename = 'demo'

    query = 'SELECT *, strftime("%d/%m/%Y", lastvisit) as lastvisit FROM ' + mydb_tablename
    queryCount = 'SELECT count(id) as nb FROM ' + mydb_tablename

    totalUnfiltered = mysqli.execute(queryCount).fetchone()[0]
    total = totalUnfiltered

     # SERVER SIDE
     # If you have set serverSide : true in your Javascript code, _GET contains 3 additionnal parameters : page, filter, sort
     # this parameters allow you to adapt your query
     #

    page = 0
    if 'page' in _GET and _GET['page'].isnumeric():
      page = int(_GET['page'])

    rowByPage = 50

    from_ = (page - 1) * rowByPage

    if 'filter' in _GET and _GET['filter'] != "":
        filter = _GET['filter']
        query += '  WHERE name like "%' + filter + '%" OR firstname like "%' + filter + '%"'
        queryCount += '  WHERE name like "%' + filter + '%" OR firstname like "%' + filter + '%"'
        cur = mysqli.execute(queryCount)
        total = cur.fetchone()[0]

    if 'sort' in _GET and _GET['sort'] != "" :
      query += " ORDER BY " + _GET['sort'] + (" DESC " if _GET['asc'] == "0" else "")

    query += " LIMIT " + str(from_) + ", " + str(rowByPage)

    print("pageCount = " + str(ceil(total / rowByPage)))
    print("total = " + str(total))
    print("totalUnfiltered = " + str(totalUnfiltered))

    grid.setPaginator(ceil(total / rowByPage), int(total), int(totalUnfiltered), None)

     # END SERVER SIDE

    print(query)

    result = mysqli.execute(query)

    ret = grid.renderJSON(result, False, False, ('data_only' not in _GET))

    mysqli.close()
    # send data to the browser

    return ret


if __name__ == "__main__":
    print(main({}))


