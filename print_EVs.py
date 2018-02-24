import time
from pathlib import Path

import ruamel.yaml as yaml
from tabulate import tabulate


def load_price_data(item):
    item_path = Path('items_pricing/', item + '.yml')
    if item_path.exists():
        with open(str(item_path), 'r') as f:
            item_pricing = yaml.load(f, Loader=yaml.Loader)

        return item_pricing


def items_price_data(crate_item_names):
    items_price = []
    price_time = []
    for item_name in crate_item_names:
        price_data = load_price_data(item_name)
        if price_data is not None:
            # price = $2.03
            items_price.append(float(price_data['median_price'][1:]))
            price_time.append(float(price_data['time']))
        else:
            items_price.append(None)
            price_time.append(None)
            print('Price data not found for {}'.format(item_name))
    return items_price, price_time


def print_EVs():
    crate_path = Path('crates/')
    crate_files = crate_path.glob('*.*')

    print('Current time:', time.asctime())
    print_data = []
    for cf in crate_files:
        with open(str(cf)) as stream:
            try:
                crate_info = yaml.load(stream, Loader=yaml.Loader)
            except yaml.YAMLError as exc:
                print(exc)

            crate_price_data = items_price_data(
                [crate_info['name']])
            crate_price = crate_price_data[0][0]
            crate_price_time = crate_price_data[1][0]

            if 'items' in crate_info:
                item_prices, item_price_times = items_price_data(
                    crate_info['items'].keys())

            if 'keys' in crate_info:
                key_prices, key_price_times = items_price_data(
                    crate_info['keys'])
                key_price = min(key_prices)
            else:
                key_price = 0

            items_weights = [a/100 for a in crate_info['items'].values()]
            items_EV = sum([p*w for p, w in zip(item_prices, items_weights)])

            now = time.time()
            price_age = (now - min(item_price_times + [crate_price_time]))/60

            EV = items_EV - key_price

            print_data.append(
                [crate_info['name'], EV, crate_price, key_price, price_age])

    headers = ['Crate', 'Open EV ($)', 'Crate ($)',
               'Key ($)', 'Price age (min)']
    print(tabulate(print_data, headers, floatfmt=".2f"))


def main():
    print_EVs()


if __name__ == '__main__':
    main()
