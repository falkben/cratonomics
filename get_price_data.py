import time
from datetime import datetime, timedelta
from pathlib import Path
from random import random

import requests
import ruamel.yaml as yaml
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient()
db = client.price_database
item_prices = db.item_prices


def get_price_data(item, appid=578080, currency=1):
    # https://steamcommunity.com/market/priceoverview/?appid=578080&currency=1&market_hash_name=Ballistic%20Mask
    url_base = 'https://steamcommunity.com/market/priceoverview/?'
    url = '{}appid={}&currency={}&market_hash_name={}'.format(
        url_base, appid, currency, item)

    r = requests.get(url)
    time.sleep(3+random())
    return r.json()


def save_price_data(item, time_thresh=10):
    now = datetime.utcnow()

    # get the latest from the database, if "fresh" enough, don't even attempt to get new data
    last_price_data = item_prices.find_one(
        {'name': item}, sort=[('datetime', -1)])

    if last_price_data is not None:
        # only freshen the data if it's older than time_thresh minutes
        if last_price_data['datetime'] + timedelta(minutes=time_thresh) > now:
            return last_price_data

    # https://steamcommunity.com/market/priceoverview/?appid=578080&currency=1&market_hash_name=Ballistic%20Mask
    item_data = get_price_data(item)

    if item_data is None or not item_data['success']:
        print("Error in getting price data for item {}".format(item))
        return None

    item_data['datetime'] = now
    item_data.pop('success')
    item_data['name'] = item

    item_prices.insert_one(item_data)

    return item_data


def get_crate_info(cf):
    with open(str(cf)) as stream:
        try:
            crate_info = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    return crate_info


def save_price_each_crate():
    crate_path = Path('crates/')
    crate_files = list(crate_path.glob('*.*'))

    # getting the total # of items for the progress bar
    tot_items = 0
    for cf in crate_files:
        crate_info = get_crate_info(cf)
        tot_items += 1  # for the crate
        tot_items += len(crate_info['items'])
        if 'keys' in crate_info:
            tot_items += len(crate_info['keys'])

    with tqdm(total=tot_items) as pbar:
        for cf in tqdm(crate_files):
            crate_info = get_crate_info(cf)

            save_price_data(crate_info['name'])
            pbar.update(1)

            if 'items' in crate_info:
                crate_items = crate_info['items']
                # print('Sum of probability of items in crate {}: {}'.format(
                #     crate_info['name'], sum(crate_items.values())))
                for item_name in crate_items.keys():
                    save_price_data(item_name)
                    pbar.update(1)
            if 'keys' in crate_info:
                crate_keys = crate_info['keys']
                for key_name in crate_keys:
                    save_price_data(key_name)
                    pbar.update(1)


def main():
    save_price_each_crate()


if __name__ == '__main__':
    main()
