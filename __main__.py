import reader, argparse, pretty_print, re
from math import inf

parser = argparse.ArgumentParser(description='Proccess a commodities csv-file')
parser.add_argument('file', metavar='F', type=str,
                    help='The commodity csv file')
parser.add_argument('--buy-diff', '-bd', nargs='?', type=int, dest='buy_diff', const=-inf,
                    help='Filters for a buy price minimum difference towards galactic average')
parser.add_argument('--sell-diff', '-sd', nargs='?', type=int, dest='sell_diff', const=-inf,
                    help='Filters for a sell price minimum difference towards galactic avery')
parser.add_argument('--supply', '-s', type=int, dest='supply',
                    help='Filters for a minimum demand/supply value')
parser.add_argument('--economies', '-e', action='store_true', dest='economies',
                    help='If present, the economies involved when trading to given station will be displayed.')
parser.add_argument('--to', '-t', type=str, dest='consumer', default='.*')
parser.add_argument('--from', '-f', type=str, dest='producer', default='.*')

args = parser.parse_args()
with open(args.file, 'r', encoding='utf8') as f:
    org_commodities = reader.read_commodities(f)
    commodities_lists = []

    if args.sell_diff is not None:
        sell_commodities = filter(
            lambda co: co.sell_avg is not None and co.sell_avg >= args.sell_diff and len(co.produced_by) > 0,
            list(org_commodities)
        )
        sell_commodities = filter(
            lambda co: True in map(lambda prod: bool(re.match(args.producer, prod)), co.produced_by),
            sell_commodities
        )
        sell_commodities = sorted(
            sell_commodities,
            key=lambda co: co.sell_avg,
            reverse=True
        )
        commodities_lists.append(sell_commodities)

    if args.buy_diff is not None:
        buy_commodities = filter(
            lambda co: co.buy_avg is not None and co.buy_avg >= args.buy_diff,
            list(org_commodities)
        )
        buy_commodities = filter(
            lambda co: True in map(lambda cons: bool(re.match(args.consumer, cons)), co.consumed_by),
            buy_commodities
        )
        buy_commodities = sorted(
            buy_commodities,
            key=lambda co: co.buy_avg,
            reverse=True
        )
        commodities_lists.append(buy_commodities)

    if len(commodities_lists) == 0:
        commodities_lists = [list(org_commodities)]

    if args.supply is not None:
        commodities_lists = [
            filter(
                lambda co: (co.demand is None or co.demand >= args.supply) and (co.supply is None or co.supply >= args.supply),
                commodities
            ) for commodities in commodities_lists
        ]

    for commodities in commodities_lists:
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
        print()

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
