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
from flask import render_template

import datetime



# Load the Pandas libraries with alias 'pd'
import pandas as pd
import re
import csv

def mutate_dict(x):
    return x.rstrip(',').strip()

def fix_the_shit(file):
    data = pd.read_csv(file, sep=';', encoding='cp1251')

    lis = data.astype(str).values.tolist()

    target = []
    for rows in lis:
        date = rows[1]
        services = re.findall(r'([^;]+?, \d+,)', rows[3])
        l = map(mutate_dict, services)
        for x in l:
            rvs = x[::-1]
            i = rvs.find(',')
            t1 = x[:-i - 1].strip()
            t2 = x[-i:].strip()
            target.append([date, t1, t2])

    #full_path = os.path.join(app.config['UPLOADED_PATH'], file.filename)
    with open('result.csv', "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(target)

app = Flask(__name__)

dropzone = Dropzone(app)

@app.route('/kamala-first-seen-clients')
def render_response():
    return render_template('kamala-first-seen-clients.html')

@app.route('/kamala-services-per-day', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        #full_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        #f.save(full_path)
        fix_the_shit(f)
        #return send_from_directory(app.config['UPLOADED_PATH'], filename=f.filename, as_attachment=True, attachment_filename=f.filename+'fixed')
    return render_template('index.html')

@app.route('/kamala-services-per-day-file')
def return_files():
    return send_file(
        'result.csv',
        mimetype='text/csv',
        attachment_filename='result'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv',
        as_attachment=True,
        cache_timeout=0
    )

if __name__ == '__main__':
    app.run(debug=True)
