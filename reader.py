import csv
from commodity import Commodity

def read_commodities(file):
    commodities = []
    reader = csv.reader(file, dialect=csv.excel, delimiter=';')
    next(reader)  # skip headline
    for line in reader:
        name = line[2]

        try:
            sell = int(line[3])
        except ValueError:
            sell = None

        try:
            buy = int(line[4])
        except ValueError:
            buy = None

        try:
            demand = int(line[5])
        except ValueError:
            demand = None

        try:
            supply = int(line[7])
        except ValueError:
            supply = None

        commodities.append(Commodity(name, sell, buy, demand, supply))

    return commodities
