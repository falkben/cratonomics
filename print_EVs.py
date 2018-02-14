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
    for item_name in crate_item_names:
        price_data = load_price_data(item_name)
        if price_data is not None:
            # price = $2.03
            items_price.append(float(price_data['lowest_price'][1:]))
        else:
            items_price.append(None)
            print('Price data not found for {}'.format(item_name))
    return items_price


def print_EVs():
    crate_path = Path('crates/')
    crate_files = crate_path.glob('*.*')

    print(time.asctime())
    print_data = []
    for cf in crate_files:
        with open(str(cf)) as stream:
            try:
                crate_info = yaml.load(stream, Loader=yaml.Loader)
            except yaml.YAMLError as exc:
                print(exc)

            crate_price = items_price_data([crate_info['name']])[0]

            if 'items' in crate_info:
                item_prices = items_price_data(crate_info['items'].keys())

            if 'keys' in crate_info:
                key_prices = items_price_data(crate_info['keys'])
            else:
                key_prices = [0]

            items_weights = [a/100 for a in crate_info['items'].values()]
            items_EV = sum([p*w for p, w in zip(item_prices, items_weights)])
            EV = items_EV - min(key_prices)

            print_data.append([crate_info['name'], EV, crate_price])

            # print('{:15}: Expected value of opening: ${: 1.02f}, Price of crate: ${:1.02f}'.format(
            #     crate_info['name'], EV, float(crate_price['lowest_price'][1:])))

    headers = ['Crate', 'EV of opening ($)', 'Crate Price ($)']
    print(tabulate(print_data, headers, floatfmt=".2f"))


def main():
    print_EVs()


if __name__ == '__main__':
    main()
