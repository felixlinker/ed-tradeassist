import sys, reader, argparse, json
from functools import reduce
from math import ceil

parser = argparse.ArgumentParser(description='Proccess a commodities csv-file')
parser.add_argument('file', metavar='F', type=str,
                    help='The commodity csv file')
parser.add_argument('--buy-diff', '-bd', type=int, dest='buy_diff',
                    help='Filters for a buy price minimum difference towards galactic average')
parser.add_argument('--sell-diff', '-sd', type=int, dest='sell_diff',
                    help='Filters for a sell price minimum difference towards galactic avery')
parser.add_argument('--supply', '-s', type=int, dest='supply',
                    help='Filters for a minimum demand/supply value')

args = parser.parse_args()
with open(args.file, 'r', encoding='utf8') as f:
    commodities = reader.read_commodities(f)

    if args.sell_diff is not None:
        commodities = filter(
            lambda x: x['sell_average'] is not None and x['sell_average'] >= args.sell_diff,
            commodities
        )
        commodities = sorted(list(commodities), key=lambda x: x['sell_average'], reverse=True)
    elif args.buy_diff is not None:
        commodities = filter(
            lambda x: x['buy_average'] is not None and x['buy_average'] >= args.buy_diff,
            commodities
        )
        commodities = sorted(list(commodities), key=lambda x: x['buy_average'], reverse=True)

    if args.supply is not None:
        commodities = filter(
            lambda x: x['demand'] is None or x['demand'] >= args.supply,
            commodities
        )
        commodities = filter(
            lambda x: x['supply'] is None or x['supply'] >= args.supply,
            commodities
        )

    commodities = list(commodities)
    if len(commodities) == 0:
        print('No commodity matches your criteria')
        sys.exit(0)

    headline_object = {}
    for key, _ in commodities[0].items():
        headline_object[key]  = key
    commodities.insert(0, headline_object)
    max_tabs = ceil(max(map(lambda x: len(x['commodity']), commodities)) / 8)

    for co in commodities:
        c_tabs = ceil(((8 * max_tabs) - len(co['commodity'])) / 8)
        s_tabs = ceil((16 - len(str(co['sell_average']))) / 8)
        b_tabs = ceil((16 - len(str(co['buy_average']))) / 8)
        print(
            co['commodity'] + ('\t' * c_tabs)
            + str(co['sell']) + '\t' + str(co['sell_average']) + ('\t' * s_tabs)
            + str(co['buy']) + '\t' + str(co['buy_average']) + ('\t' * b_tabs)
            + str(co['demand']) + '\t' + str(co['supply'])
        )
