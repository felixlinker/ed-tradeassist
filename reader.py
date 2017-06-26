import os, csv, inspect, re

AVERAGES = {}
TYPES = []
__file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

with open(os.path.join(__file_dir, 'prices.csv'), 'r', encoding='utf8') as f:
    reader = csv.reader(f, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        AVERAGES[line[0]] = {
            'price': int(line[1]),
            'produced_by': line[2],
            'consumed_by': line[3]
        }

with open(os.path.join(__file_dir, 'types.csv'), 'r', encoding='utf8') as f:
    reader = csv.reader(f, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        TYPES.append(line[0] + ' (Surface)')
        TYPES.append(line[0] + ' (Space)')

def reduce_types(type_string):
    reduced = set()
    types = type_string.split(',')
    for t in types:
        t = t.strip()
        if t.startswith('!'):
            reduced -= reduce_types(t[1:])
        else:
            pattern = ''
            if t.startswith('.*'):
                pattern = t[:2]
                t = t[2:]
            pattern += re.escape(t)

            reduced |= set(filter(lambda x: re.search(pattern, x), TYPES))

    return reduced

def read_commodities(file):
    commodities = []
    reader = csv.reader(file, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        co = { 'commodity': line[2] }

        co['average'] = AVERAGES[co['commodity']]['price']

        try:
            co['sell'] = int(line[3])
            co['sell_average'] = co['sell'] - co['average']
        except ValueError:
            co['sell'] = None
            co['sell_average'] = None

        try:
            co['buy'] = int(line[4])
            co['buy_average'] = co['average'] - co['buy']
        except ValueError:
            co['buy'] = None
            co['buy_average'] = None

        try:
            co['demand'] = int(line[5])
        except ValueError:
            co['demand'] = None

        try:
            co['supply'] = int(line[7])
        except ValueError:
            co['supply'] = None

        commodities.append(co)

    return commodities
