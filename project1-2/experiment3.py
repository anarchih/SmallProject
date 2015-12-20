import pandas as pd
import datetime as dt
from subprocess import check_output
import matplotlib.pyplot as plt

data = pd.read_csv("sorted.tsv", sep="\t")
data = data.rename(columns = {'經度座標':'x'})
data = data.rename(columns = {'緯度座標':'y'})
data = data.rename(columns = {'發病日期':'date'})

# dtime = pd.DataFrame([[dt.datetime.strptime('2015/' + i, "%Y/%m/%d")] for i in data['發病日期']], columns=['date'])
# data = data.join(dtime)
# del data['發病日期']
w = dt.datetime.strptime('2015/' + data.date[0], "%Y/%m/%d").isocalendar()[1]
# w = data.date[0].week
last = 0
week_quantum = 2
for i, k in enumerate(data.date):
    if dt.datetime.strptime('2015/' + k, "%Y/%m/%d").isocalendar()[1] - w >= week_quantum:
        t = data[last:i]
        last = i
        t.to_csv("tmp.tsv", sep="\t", index=False)
        q = check_output(['pypy', 'gene.py', 'tmp.tsv'])
        print(q.decode('utf-8').split('\n')[-3])
        print(q.decode('utf-8').split('\n')[-2])

        w += week_quantum

