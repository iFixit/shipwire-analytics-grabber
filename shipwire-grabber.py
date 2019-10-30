#!/usr/bin/env python3
import os
import datetime
import pytz
import iso8601
import json

from shipwire import Shipwire
from pymongo import MongoClient

mst = pytz.timezone("America/Phoenix")
now = datetime.datetime.now(tz=mst)

today = now.date()
yesterday = datetime.datetime.combine(today - datetime.timedelta(days=1), datetime.time.min)
today = datetime.datetime.combine(yesterday + datetime.timedelta(days=1), datetime.time.min)

mongo = MongoClient(os.environ['MONGODB_URI'])
shipwire = Shipwire(
            os.environ['SHIPWIRE_USER'],
            os.environ['SHIPWIRE_PASSWORD'],
            host='api.shipwire.com')

def get_orders(start_date, stop_date):
    res = shipwire.orders.list(
            json=None,
            completedAfter=start_date.astimezone(mst).isoformat(),
            completedBefore=stop_date.astimezone(mst).isoformat(),
            expand="items")

    return list(map(lambda item: item['resource'], res.all()))

def get_stock():
    res = shipwire.stock.products()
    stock = list(map(lambda item: item['resource'], res.all()))

    for product in stock:
        product['date'] = yesterday

    return stock

def clean_order(order):
    def clean_tree(doc):
        """Takes a document and recursively flattens "resource" objects"""
        if 'resource' in doc:
            return clean_tree(doc['resource'])

        if 'resourceLocation' in doc:
            return None

        if type(doc) is dict:
            for key in doc:
                if type(doc[key]) is dict:
                    doc[key] = clean_tree(doc[key])
                elif type(doc[key]) is list:
                    return list(map(clean_tree, doc[key]))

        return {k: v for k, v in doc.items() if v is not None}

    def convert_dates(doc):
        """Converts ISO8601 time strings to Datetime objects for MongoDB"""
        for date in doc['events']:
            doc['events'][date] = iso8601.parse_date(doc['events'][date])

        doc['lastUpdatedDate'] = iso8601.parse_date(doc['lastUpdatedDate'])
        doc['processAfterDate'] = iso8601.parse_date(doc['processAfterDate'])

        return doc

    return convert_dates(clean_tree(order))

orders_collection = mongo.warehouse.shipwire_orders
stock_collection = mongo.warehouse.shipwire_stock

for order in get_orders(yesterday, today):
    orders_collection.save(clean_order(order))

for stock in get_stock():
    stock_collection.save(stock)
