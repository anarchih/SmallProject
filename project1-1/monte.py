import pandas as pd
import datetime as dt
import random


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def randrange(Min, Max):
    return random.random() * (Max - Min) + Min

def evaluate(ind, dist, data):
    count = 0
    for p1 in zip(data.x, data.y):
        for j, p2 in enumerate(ind):
            if distance(p1, p2) < dist:
                count += 1
                break
    return count

data = pd.read_csv("data.tsv", sep="\t")
data = data.rename(columns = {'經度座標':'x'})
data = data.rename(columns = {'緯度座標':'y'})
dtime = pd.DataFrame([[dt.datetime.strptime('2015/' + i, "%Y/%m/%d")] for i in data['發病日期']], columns=['date'])
data = data.join(dtime)
del data['發病日期']


k = 10
Max = 0
xmin = data.x.min()
ymin = data.y.min()
xmax = data.x.max()
ymax = data.y.max()

for i in range(0, 3000):
    ind = [(randrange(xmin, xmax), randrange(ymin, ymax)) for i in range(0, k)]

    value = evaluate(ind, 0.02, data)
    if Max < value:
        Max = value
        print(Max)
