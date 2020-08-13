# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os

from flask import Flask, render_template, request
from flask_dropzone import Dropzone
from flask import send_file, send_from_directory

from flask import Flask
from flask_dropzone import Dropzone
from flask import *

import servicesperday
from firstseenclients import get_api_data

import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
)



dropzone = Dropzone(app)

@app.route('/kamala-first-seen-clients')
def render_response():
    return get_api_data()

@app.route('/kamala-services-per-day', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        servicesperday.write_file(
            os.path.join(app.config['UPLOADED_PATH'], 'result.csv'),
            servicesperday.convert_to_csv(f)
        )
    return render_template('index.html')

@app.route('/kamala-services-per-day-file')
def return_files():
    return send_file(
        os.path.join(app.config['UPLOADED_PATH'], 'result.csv'),
        mimetype='text/csv',
        attachment_filename='result'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv',
        as_attachment=True,
        cache_timeout=0
    )

if __name__ == '__main__':
    app.run(debug=True)
