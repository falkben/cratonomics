
from pathlib import Path

import ruamel.yaml as yaml


def load_price_data(item):
    item_path = Path('items_pricing/', item + '.yml')
    if item_path.exists():
        with open(item_path, 'r') as f:
            item_pricing = yaml.load(f, Loader=yaml.Loader)

        return item_pricing


def print_EVs():
    crate_path = Path('crates/')
    crate_files = crate_path.glob('*.*')

    for cf in crate_files:
        with open(cf) as stream:
            try:
                crate_info = yaml.load(stream, Loader=yaml.Loader)
            except yaml.YAMLError as exc:
                print(exc)

            crate_price = load_price_data(crate_info['name'])
            if 'items' in crate_info:
                crate_items = crate_info['items']
                items_weight_prices = []
                # print('Sum of probability of items in crate {}: {}'.format(
                #     crate_info['name'], sum(crate_items.values())))
                for item_name, item_prob in crate_items.items():
                    price_data = load_price_data(item_name)
                    if price_data is not None:
                        item_price = float(price_data['lowest_price'][1:])
                        items_weight_prices.append(item_price * item_prob/100)
                    else:
                        print('Price data not found for {}'.format(item_name))
                print('{}: Items: ${:.02f}, Market: ${:.02f}'.format(crate_info['name'], sum(
                    items_weight_prices), float(crate_price['lowest_price'][1:])))


def main():
    print_EVs()


if __name__ == '__main__':
    main()
