#!/usr/bin/env python

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference
import socket
import re

# init app
app = Flask(__name__)

def connect():
    connection = MongoClient(["mongo1", "mongo2", "mongo3"])
    db = connection.app_database
    collection = db.homicide_rates 
    return db, collection

def reverse(ip):
    return socket.gethostbyaddr(ip)[0]

def is_valid_ipv4(ip_address):
    """ Validates IPv4 addresses. """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip_address) is not None

@app.route('/')
def index():
    if request.method == 'GET':
        db, collection = connect()
        rates = collection.find()
        host = db.connection.host
        if is_valid_ipv4(db.connection.host):
            host = reverse(host)
        return render_template('index.html', count=rates.count(), host=host)

@app.route('/list')
def list():
    name = request.args.get('name')
    args={}
    if name:
        args['country'] = name
    if request.method == 'GET':
        db, collection = connect()
        rates = collection.find(args)
        return render_template('list.html', rates=rates)

@app.route('/about')
def about():
    if request.method == 'GET':
        return render_template('about.html')

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=80)
