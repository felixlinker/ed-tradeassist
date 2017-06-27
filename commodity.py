import os, csv, inspect, re


TYPES = []
AVERAGES = {}
__file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

with open(os.path.join(__file_dir, 'types.csv'), 'r', encoding='utf8') as f:
    reader = csv.reader(f, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        TYPES.append(line[0] + ' (Surface)')
        TYPES.append(line[0] + ' (Space)')

def reduce_types(type_string):
    reduced = set()
    if type_string == '':
        return reduced
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

with open(os.path.join(__file_dir, 'prices.csv'), 'r', encoding='utf8') as f:
    reader = csv.reader(f, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        AVERAGES[line[0]] = {
            'price': int(line[1]),
            'produced_by': reduce_types(line[2]),
            'consumed_by': reduce_types(line[3])
        }

class Commodity:

    def __init__(self, name, sell, buy, demand, supply):
        try:
            AVERAGES[name]
        except KeyError:
            raise ValueError('The commodity "' + name + '" does not exist')
        base_commodity = AVERAGES[name]

        self.name = name
        self.sell = sell
        self.sell_avg = None if sell is None else sell - base_commodity['price']
        self.buy = buy
        self.buy_avg = None if buy is None else base_commodity['price'] - buy
        self.demand = demand
        self.supply = supply
        self.average = base_commodity['price']
        self.produced_by = base_commodity['produced_by']
        self.consumed_by = base_commodity['consumed_by']
