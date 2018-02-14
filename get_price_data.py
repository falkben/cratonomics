import time
from pathlib import Path

import ruamel.yaml as yaml
import requests
from tqdm import tqdm

# use database to store the price data instead of flat files


# # https://realpython.com/blog/python/introduction-to-mongodb-and-python/
# import pymongo
# # in another terminal start run mongod
# from pymongo import MongoClient
# client = MongoClient()
# db = client.price_data


def get_price_data(item, appid=578080, currency=1):
    # https://steamcommunity.com/market/priceoverview/?appid=578080&currency=1&market_hash_name=Ballistic%20Mask
    url_base = 'https://steamcommunity.com/market/priceoverview/?'
    url = '{}appid={}&currency={}&market_hash_name={}'.format(
        url_base, appid, currency, item)

    r = requests.get(url)
    time.sleep(3)
    return r.json()


def save_price_data(item, time_thresh=10):
    item_path = Path('items_pricing/', item + '.yml')

    now = time.time()

    if item_path.exists():
        # load old price data
        with open(str(item_path), 'r') as f:
            try:
                old_item_pricing = yaml.load(f, Loader=yaml.Loader)
            except yaml.YAMLError as exc:
                print(exc)

        # only freshen the data if it's older than time_thresh minutes
        if old_item_pricing['time'] + time_thresh*60 > now:
            return old_item_pricing

    # https://steamcommunity.com/market/priceoverview/?appid=578080&currency=1&market_hash_name=Ballistic%20Mask
    item_data = get_price_data(item)
    if item_data['success'] is False:
        print('item not found {}'.format(item))
        return None

    item_data['time'] = now
    item_data.pop('success')

    with open(str(item_path), 'w') as f:
        yaml.dump(item_data, f, default_flow_style=False)

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
    crate_files = crate_path.glob('*.*')

    # getting the total # of items for the progress bar
    tot_items = 0
    for cf in crate_files:
        crate_info = get_crate_info(cf)
        tot_items += 1  # for the crate
        tot_items += len(crate_info['items'])
        if 'keys' in crate_info:
            tot_items += len(crate_info['keys'])

    with tqdm(total=tot_items) as pbar:
        crate_files = crate_path.glob('*.*')
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
