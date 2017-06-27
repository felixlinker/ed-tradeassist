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
parser.add_argument('--economies', '-e', action='store_true', dest='economies',
                    help='If present, the economies involved when trading to given station will be displayed.')

args = parser.parse_args()
with open(args.file, 'r', encoding='utf8') as f:
    org_commodities = reader.read_commodities(f)
    commodities = list(org_commodities)

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

    if args.economies:
        producer_mapping = dict()
        consumer_mapping = dict()
        for co in org_commodities:
            if co.sell_avg is not None:
                for producer in co.produced_by:
                    producer_mapping.setdefault(producer, list())\
                        .append((co.name, co.sell_avg))

            if co.buy_avg is not None:
                for consumer in co.consumed_by:
                    consumer_mapping.setdefault(consumer, list())\
                        .append((co.name, co.buy_avg))

        print()
        producer_matrix = []
        for k, v in producer_mapping.items():
            v = sorted(v, key=lambda co: co[1], reverse=True)
            v_values = [co[1] for co in v]
            producer_matrix.append([
                k,
                sum(v_values) / len(v),
                max(v_values),
                len(v),
                [co[0] for co in v][:3]
            ])
        producer_matrix = sorted(
            producer_matrix,
            key=lambda prod: prod[1],
            reverse=True
        )
        producer_matrix.insert(0, ['Producer', 'Average Profit', 'Peak Profit', 'Commodities Available', 'Best Three'])
        pretty_print.write(producer_matrix)

        print()
        consumer_matrix = []
        for k, v in consumer_mapping.items():
            v = sorted(v, key=lambda co: co[1], reverse=True)
            v_values = [co[1] for co in v]
            consumer_matrix.append([
                k,
                sum(v_values) / len(v),
                max(v_values),
                len(v),
                [co[0] for co in v][:3]
            ])
        consumer_matrix = sorted(
            consumer_matrix,
            key=lambda con: con[1],
            reverse=True
        )
        consumer_matrix.insert(0, ['Consumer', 'Average Profit', 'Peak Profit', 'Commodities Available', 'Best Three'])
        pretty_print.write(consumer_matrix)
