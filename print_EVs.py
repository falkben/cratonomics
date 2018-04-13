import math
import sys
import time
from datetime import datetime
from pathlib import Path

import ruamel.yaml as yaml
from pymongo import MongoClient
from tabulate import tabulate

CLIENT = MongoClient(serverSelectionTimeoutMS=3)
# check if mongod is running
try:
    CLIENT.server_info()
except Exception as e:
    print(e)
    sys.exit()

DB = CLIENT.price_database
ITEM_PRICES_TABLE = DB.item_prices


def load_price_data(item):
    return ITEM_PRICES_TABLE.find_one(
        {'name': item}, sort=[('datetime', -1)])


def items_price_data(item_names):
    items_prices = []
    price_times = []
    for item_name in item_names:
        price_data = load_price_data(item_name)
        if price_data is not None:
            # price = $2.03
            try:
                items_prices.append(float(price_data['median_price'][1:]))
                price_times.append(price_data['datetime'])
            except Exception as e:
                print('Error in retrieving data for {} with error: {}'.format(
                    item_name, e))
        else:
            items_prices.append(None)
            price_times.append(None)
            print('Price data not found for {}'.format(item_name))
    return items_prices, price_times


def process_crate(crate_fname):
    with open(str(crate_fname)) as stream:
        try:
            crate_info = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
            return None

    crate_price_data = items_price_data(
        [crate_info['name']])
    crate_price = crate_price_data[0][0]
    crate_price_time = crate_price_data[1][0]

    if 'items' in crate_info:
        items_prices, items_price_times = items_price_data(
            crate_info['items'].keys())

    if 'key' in crate_info:
        key_price = list(crate_info['key'].values())[0]
    else:
        key_price = 0

    items_weights = [a / 100 for a in crate_info['items'].values()]
    if not math.isclose(sum(items_weights), 1, rel_tol=2e-1):
        print('{} has weights that don''t sum to 1. Sum weights: {}'.format(
            crate_info['name'], sum(items_weights)))
    items_EV = sum([p * w for p, w in zip(items_prices, items_weights)])

    now = datetime.utcnow()
    price_age = now - min(items_price_times + [crate_price_time])
    price_age = round(price_age.total_seconds() / 60)

    EV = items_EV - key_price

    return [crate_info['name'], EV, crate_price, key_price, price_age]


def print_EVs():
    crate_path = Path('crates/')
    crate_files = crate_path.glob('*.*')

    print('Current time:', time.asctime())
    print_data = []
    for cf in crate_files:
        crate_result = process_crate(cf)
        if crate_result is not None:
            print_data.append(crate_result)

    print_data.sort(key=lambda x: x[0])

    headers = ['Crate', 'Open EV ($)', 'Crate ($)',
               'Key ($)', 'Price age (max)']
    print(tabulate(print_data, headers, floatfmt=".2f"))


def main():
    print_EVs()


if __name__ == '__main__':
    main()
