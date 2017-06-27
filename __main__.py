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
            lambda co: co.sell_avg is not None and co.sell_avg >= args.sell_diff,
            commodities
        )
        commodities = sorted(list(commodities), key=lambda x: x['sell_average'], reverse=True)
    elif args.buy_diff is not None:
        commodities = filter(
            lambda co: co.buy_avg is not None and co.buy_avg >= args.buy_diff,
            commodities
        )
        commodities = sorted(list(commodities), key=lambda x: x.buy_avg, reverse=True)

    if args.supply is not None:
        commodities = filter(
            lambda co: co.demand is None or co.demand >= args.supply,
            commodities
        )
        commodities = filter(
            lambda co: co.supply is None or co.supply >= args.supply,
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
    max_tabs = ceil(max(map(lambda x: len(x.name), commodities)) / 8)

    for co in commodities:
        c_tabs = ceil(((8 * max_tabs) - len(co.name)) / 8)
        s_tabs = ceil((16 - len(str(co.sell_avg))) / 8)
        b_tabs = ceil((16 - len(str(co.buy_avg))) / 8)
        print(
            co.commodity + ('\t' * c_tabs)
            + str(co.sell) + '\t' + str(co.sell_avg) + ('\t' * s_tabs)
            + str(co.buy) + '\t' + str(co.buy_avg) + ('\t' * b_tabs)
            + str(co.demand) + '\t' + str(co.supply)
        )
