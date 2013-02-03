#!/usr/bin/env python

"""
Load data into master mongo database
"""

from pymongo import MongoClient
import csv
import sys

def connect():
    connection = MongoClient("mongo1")
    db = connection.app_database
    collection = db.homicide_rates
    return db, collection

def load_data(file):
    db, collection = connect()
    with open(file, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in datareader:
            print row
            collection.insert({"country": row[0],
                               "year": row[1],
                               "count": row[2],
                               "rate": row[3],
                               "source": row[4],
                               "source_type": row[5]})

if __name__ == '__main__':
    load_data(sys.argv[1])
