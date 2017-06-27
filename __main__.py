import sys, reader, argparse, json, pretty_print

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
        commodities = sorted(list(commodities), key=lambda co: co.sell_avg, reverse=True)
    elif args.buy_diff is not None:
        commodities = filter(
            lambda co: co.buy_avg is not None and co.buy_avg >= args.buy_diff,
            commodities
        )
        commodities = sorted(list(commodities), key=lambda co: co.buy_avg, reverse=True)

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

    print_matrix = [['Commodity', 'Sell', 'Sell Difference', 'Buy',
                    'Buy Difference', 'Demand', 'Supply']]
    print_matrix.extend(list(map(
        lambda co: [
            co.name,
            co.sell,
            co.sell_avg,
            co.buy,
            co.buy_avg,
            co.demand,
            co.supply
        ],
        commodities
    )));
    pretty_print.write(print_matrix)
