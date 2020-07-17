#!/usr/bin/env python3
import json
import logging
import os

import iso8601
import pytz
from pymongo import MongoClient
from shipwire import Shipwire

from dates import get_run_dates, get_yesterday, mst

logging.basicConfig()
log = logging.getLogger("Shipwire Grabber")
log.setLevel(logging.INFO)

start_time, end_time = get_run_dates()

mongo = MongoClient(os.environ["MONGODB_URI"])
shipwire = Shipwire(
    os.environ["SHIPWIRE_USER"],
    os.environ["SHIPWIRE_PASSWORD"],
    host="api.shipwire.com",
    raise_on_errors=True,
)


def get_orders(start_date, stop_date):
    res = shipwire.orders.list(
        json=None,
        completedAfter=start_date.astimezone(mst).isoformat(),
        completedBefore=stop_date.astimezone(mst).isoformat(),
        expand="items",
    )

    return list(map(lambda item: item["resource"], res.all()))


def get_stock():
    res = shipwire.stock.products(json=None)
    stock = list(map(lambda item: item["resource"], res.all()))

    for product in stock:
        product["date"] = get_yesterday()

    return stock


def clean_order(order):
    def clean_tree(doc):
        """Takes a document and recursively flattens "resource" objects"""
        if "resource" in doc:
            return clean_tree(doc["resource"])

        if "resourceLocation" in doc:
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
        for date in doc["events"]:
            doc["events"][date] = iso8601.parse_date(doc["events"][date])

        doc["lastUpdatedDate"] = iso8601.parse_date(doc["lastUpdatedDate"])
        doc["processAfterDate"] = iso8601.parse_date(doc["processAfterDate"])

        return doc

    return convert_dates(clean_tree(order))


orders_collection = mongo.warehouse.shipwire_orders
stock_collection = mongo.warehouse.shipwire_stock

orders = get_orders(start_time, end_time)
log.info("Found %d orders", len(orders))
for order in orders:
    orders_collection.save(clean_order(order))


# This isn't 100% reliable, but should be safe enough in Airflow.  It
# keeps the stock from getting updated during backfills, as the stock
# data isn't backfillable.
if start_time == get_yesterday():
    stocks = get_stock()
    log.info("Found %d stock values", len(stocks))
    for stock in stocks:
        stock_collection.save(stock)
