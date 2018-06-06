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

from flask import Flask, render_template, request, json, redirect
app = Flask(__name__)
app.debug = True

_base_path = '/editablegrid'

@app.route(_base_path+'/css/<path:path>')
def css_files(path):
    return app.send_static_file('css/' + path)

@app.route(_base_path+'/js/<path:path>')
def js_files(path):
    return app.send_static_file('js/' + path)

@app.route('/')
def hello():
    return redirect(_base_path+"/", code=302)

@app.route(_base_path+'/', methods=['GET'])
def index():
    plot_svg = ''
    plot_code = ''
    if 'style' in request.args:
        form_defaults = dict(request.args)  # get all current entries from form
        plot_code = PlotHandler.BuildPlotCode(form_defaults)
        glo = {'ret':''}
        exec(plot_code, glo)
        plot_svg = glo['ret']
    else:
        form_defaults = {}
        print('first')
    return render_template('index.html', form_defaults=form_defaults)

@app.route(_base_path+'/loaddata.py', methods=['GET'])
def _loaddata():
    import loaddata
    data = loaddata.main(request.args)
#     with open("data.json", "w") as file:
#         file.write(data)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route(_base_path+'/add.py', methods=['POST'])
def _add():
    import add
    data = add.main(request.form)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='text/plain'
    )
    return response

@app.route(_base_path+'/update.py', methods=['POST'])
def _update():
    import update
    data = update.main(request.values)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='text/plain'
    )
    return response

@app.route(_base_path+'/delete.py', methods=['POST'])
def _delete():
    print("delete")
    import delete
    data = delete.main(request.values)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='text/plain'
    )
    return response

if __name__ == "__main__":
    app.run()
