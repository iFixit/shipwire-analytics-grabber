#!/usr/bin/env python3
import os
import datetime

from shipwire import Shipwire
from pymongo import MongoClient

yesterday = datetime.datetime.combine(
                datetime.date.today() - datetime.timedelta(days=1),
                datetime.time.min)
today = yesterday + datetime.timedelta(days=1)

mongo = MongoClient(os.environ['MONGODB_URI'])
shipwire = Shipwire(
            os.environ['SHIPWIRE_USER'],
            os.environ['SHIPWIRE_PASSWORD'],
            host='api.shipwire.com')

def get_orders(start_date, stop_date):
    res = shipwire.orders.list(
            completedAfter=start_date.astimezone().isoformat(),
            completedBefore=stop_date.astimezone().isoformat(),
            expand="items")

    return list(map(lambda item: item['resource'], res.all()))

def get_stock():
    res = shipwire.stock.products()
    stock = list(map(lambda item: item['resource'], res.all()))

    for product in stock:
        product['date'] = yesterday

    return stock

orders_collection = mongo.warehouse.shipwire_orders
stock_collection = mongo.warehouse.shipwire_stock

for order in get_orders(yesterday, today):
    orders_collection.save(order)

for stock in get_stock():
    stock_collection.save(stock)
