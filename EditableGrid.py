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

# import xml.dom
import json

def default(o):
    if isinstance(o, bytes):
        return o.decode("utf-8")
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    o.__class__.__name__)

class EditableGrid():
    def __init__(self, encoding="utf-8", writeColumnNames=False, formatXML=False):
        self.columns = {}
        assert encoding == "utf-8", "%s encoding not implemented" % (encoding,)
        self.encoding = encoding
        self.writeColumnNames = writeColumnNames  # write column names in XML and JSON (set to False to save bandwidth)
        assert formatXML == False, "XML not implemented"
        self.formatXML = formatXML
        self.paginator = None

    def getColumnLabels(self):
        labels = {}
        for (name, column) in self.columns.items():
            labels[name] = column['label']
        return labels


    def getColumnFields(self):
        fields = {}
        for (name, column) in self.columns.items():
            fields[name] = column['field']
        return fields


    def getColumnTypes(self):
        types = {}
        for (name, column) in self.columns.items():
            types[name] = column['type']
        return types


    def getColumnValues(self):
        values = {}
        for (name, column) in self.columns.items():
            values[name] = column['values']
        return values


    def addColumn(self, name, label, type, values=None, editable=True, field=None, bar=True, hidden=False):
        self.columns[name] = {
            "field" : field if field != None else name,
            "label" : label,
            "type" : type,
            "editable" : editable,
            "bar" : bar,
            "hidden" : hidden,
            "values" : values}


    def setHiddenColumns(self, columns):
        for column in columns:
            if (isset(self.columns[column])):
                self.columns[column]['hidden'] = True


     #
     #  Set parameters needed for server-side pagination
     #  @param integer pageCount number of pages
     #  @param integer totalRowCount total numer of rows in all pages
     #  @param integer unfilteredRowCount total number of rows, not taking the filter into account
     #
    def setPaginator(self, pageCount, totalRowCount, unfilteredRowCount, customAttributes=None):
        self.paginator = {
            'pagecount' : pageCount,
            'totalrowcount' : totalRowCount,
            'unfilteredrowcount' : unfilteredRowCount}
        if (customAttributes is not None):
            for (key, value) in customAttributes.items():
                self.paginator[key] = value

    def _getRowField(self, row, field, row_headers=None):
        if field in row_headers:
            index = row_headers.index(field)
            value = row[index]
        elif type(row) == dict:
            value = row[field]
        elif hasattr(row, 'field'):
            value = row.field
        else:
            value = None
        # is_array(row) ? (isset(row[field]) ? row[field] : None) : (isset(row.field) ? row.field : None)
        # to avoid any issue with javascript not able to parse XML, ensure data is valid for encoding
        return value.encode("utf-8") if isinstance(value, str) else value
        # @iconv(self.encoding, "utf-8#IGNORE", value)

    @staticmethod
    def mapToArray(map):
        # convert PHP's associative array in Javascript's array of objects
        if map == None: return None
        array = []
        for (k, v) in  map.items():
            if isinstance(v, (list, dict)):
                array.append({'label' : str(k), 'values' : self.mapToArray(v) })
            else:
                array.append({'value' : str(k), 'label' : v})
        return array

    def getJSON(self, rows=False, customRowAttributes=False, encodeCustomAttributes=False, includeMetadata=True):
        pojo = self.getPOJO(rows, customRowAttributes, encodeCustomAttributes, includeMetadata)
        return json.dumps(pojo, default=default)

    def getPOJO(self, rows=False, customRowAttributes=False, encodeCustomAttributes=False, includeMetadata=True):
        results = {}

        if (includeMetadata) :

            results['metadata'] = []
            for (name, info) in self.columns.items() :
                results['metadata'].append({
                "name" : name,
                "label" : info['label'],
                "datatype" : info['type'],
                "bar" : info['bar'],
                "hidden" : info['hidden'],
                "editable" : info['editable'],
                "values" : self.mapToArray(info['values'])
                })

        if (self.paginator != None):
            results['paginator'] = self.paginator

        results['data'] = []
        row_headers = []
        for col_info in rows.description:
            row_headers.append(col_info[0])
        for row in rows:
            results['data'].append(self.getRowPOJO(row, row_headers, customRowAttributes, encodeCustomAttributes))

        return results


    def getRowPOJO(self, row, row_headers, customRowAttributes, encodeCustomAttributes):
        if (self.writeColumnNames):
            value_type = {}
        else:
            value_type = []
        data = {"id" : self._getRowField(row, 'id', row_headers), "values" : value_type}
        if (customRowAttributes):
            for (name, field) in customRowAttributes:
                if encodeCustomAttributes:
                    data[name] = base64_encode(self._getRowField(row, field, row_headers))
                else:
                    data[name] = self._getRowField(row, field, row_headers)

        for name, info in self.columns.items():
            field = info['field']
            if (self.writeColumnNames):
                data["values"][name] = self._getRowField(row, field, row_headers)
            else:
                data["values"].append(self._getRowField(row, field, row_headers))
        return data


    def renderJSON(self, rows=False, customRowAttributes=False, encodeCustomAttributes=False, includeMetadata=True):
        return (self.getJSON(rows, customRowAttributes, encodeCustomAttributes, includeMetadata))

    @staticmethod
    def parseInt(string) :
        return intval(array[0]) if preg_match('/[-+]{0,1}(\d+)/', string, array) else None


    @staticmethod
    def parseFloat(string) :
        return floatval(array[0]) if preg_match('/[-+]{0,1}([\d\.]+)/', string, array) else None


    @staticmethod
    def repeat(len, pattern=" "):
        str = ""
        for i in range(len) :
            str += pattern
        return str


    def parseColumnType(self, type, unitTranslations=False):
        info = {
            'unit' : '',
            'precision' :-1,
            'decimal_point' : ',',
            'thousands_separator' : '.',
            'unit_before_number' : False,
            'nansymbol' : ''
            }

        parts = {}

        if (preg_match("/(.*)\((.*),(.*),(.*),(.*),(.*),(.*)\)/", type, parts)):
            parts = array_map('trim', parts)
            info['datatype'] = parts[1]
            info['unit'] = parts[2]
            info['precision'] = self.parseInt(parts[3])
            info['decimal_point'] = parts[4]
            info['thousands_separator'] = parts[5]
            info['unit_before_number'] = parts[6] == '1'
            info['nansymbol'] = parts[7]


        elif (preg_match("/(.*)\((.*),(.*),(.*),(.*),(.*)\)/", type, parts)) :
            parts = array_map('trim', parts)
            info['datatype'] = parts[1]
            info['unit'] = parts[2]
            info['precision'] = self.parseInt(parts[3])
            info['decimal_point'] = parts[4]
            info['thousands_separator'] = parts[5]
            info['unit_before_number'] = parts[6] == '1'


        elif (preg_match("/(.*)\((.*),(.*),(.*)\)/", type, parts)) :
            parts = array_map('trim', parts)
            info['datatype'] = parts[1]
            info['unit'] = parts[2]
            info['precision'] = self.parseInt(parts[3])
            info['nansymbol'] = parts[4]


        elif (preg_match("/(.*)\((.*),(.*)\)/", type, parts)) :
            parts = array_map('trim', parts)
            info['datatype'] = parts[1]
            info['unit'] = parts[2]
            info['precision'] = self.parseInt(parts[3])


        elif (preg_match("/(.*)\((.*)\)/", type, parts)) :
            parts = array_map('trim', parts)
            info['datatype'] = parts[1]
            precision = self.parseInt(parts[2])
            if (precision == None):
                info['unit'] = parts[2]
            else:
                info['precision'] = precision


        if (info['decimal_point'] == 'comma'):
            info['decimal_point'] = ','
        if (info['decimal_point'] == 'dot') :
            info['decimal_point'] = '.'
        if (info['thousands_separator'] == 'comma') :
            info['thousands_separator'] = ','
        if (info['thousands_separator'] == 'dot') :
            info['thousands_separator'] = '.'

        if (info['unit'] and isset(unitTranslations[info['unit']])) :
            info['unit'] = unitTranslations[info['unit']]

        return info
