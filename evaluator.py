# import pandas as pd
import datetime as dt
# import matplotlib.pyplot as plt
from collections import Counter
import csv

class Cluster(object):
    def __init__(self, capacity):
        self.week = [0] * 60

class Evaluater(object):
    def __init__(self, filename, k, dist, capacity, date_range):
        self.data = self.read_tsv(filename)
        self.k = k
        self.dist = dist
        self.capacity = capacity
        self.date_range = dt.timedelta(date_range)
        self.cluster = Cluster(capacity)
        self.xmin = min(self.data['x'])
        self.xmax = max(self.data['x'])
        self.ymin = min(self.data['y'])
        self.ymax = max(self.data['y'])
        self.labels_ = [0 for i in range(len(self.data['x']))]

    def read_tsv(self, filename):
        data = {'x': [], 'y': [], 'date':[]}
        f = open(filename, "r")
        f.readline()
        for row in csv.reader(f, delimiter='\t'):
            data['x'].append(float(row[9]))
            data['y'].append(float(row[10]))
            data['date'].append(dt.datetime.strptime('2015/' + row[5], "%Y/%m/%d"))
        return data
        # data = pd.read_csv(filename, sep="\t")
        # # rows = random.sample(list(data.index), 5000)
        # # data = data.ix[rows]
        # data = data.rename(columns = {'經度座標':'x'})
        # data = data.rename(columns = {'緯度座標':'y'})

        # dtime = pd.DataFrame([[dt.datetime.strptime('2015/' + i, "%Y/%m/%d")] for i in data['發病日期']], columns=['date'])
        # data = data.join(dtime)
        # del data['發病日期']

        # data = data.sort(['date'])
        # data = data.reset_index()
        # return data

    def evaluate(self, ind):
        count = 0
        for p1 in zip(self.data['x'], self.data['y']):
            for j, p2 in enumerate(ind):
                if self.distance(p1, p2) < self.dist:
                    count += 1
                    break
        return count,

    def eval(self, ind):
        count = 0
        latest_date = [dt.datetime(1990, 1, 1)] * self.k
        sum_capacity = [0] * self.k
        tmp = [[0] * self.date_range.days for i in range(self.k)]
        for i, p1 in enumerate(zip(self.data['x'], self.data['y'])):
            c = self.find_data_belongs_to(p1, ind)
            if c != 10000:
                date_gap = self.data['date'][i] - latest_date[c]
                latest_date[c] = self.data['date'][i]
                if date_gap >= self.date_range:
                    sum_capacity[c] = 1
                    tmp[c] = [0] * self.date_range.days
                    tmp[c][0] = 1
                    count += 1
                else:
                    t = [0] * date_gap.days + tmp[c][0:self.date_range.days - date_gap.days]
                    t[0] += 1
                    sum_c = sum(t)
                    if sum_c <= self.capacity:
                        tmp[c] = t
                        sum_capacity[c] = sum_c
                        count += 1
        return count,

    def find_data_belongs_to(self, p1, ind):
        current_cluster = 10000
        Min = 10000
        for j, p2 in enumerate(ind):
            dist = self.distance(p1, p2)
            if dist < self.dist and dist < Min:
                Min = dist
                current_cluster = j
        return current_cluster

    def distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def calc_labels(self, ind):
        count = 0
        latest_date = [dt.datetime(1990, 1, 1)] * self.k
        sum_capacity = [0] * self.k
        tmp = [[0] * self.date_range.days for i in range(self.k)]
        for i, p1 in enumerate(zip(self.data['x'], self.data['y'])):
            c = self.find_data_belongs_to(p1, ind)
            if c != 10000:
                date_gap = self.data['date'][i] - latest_date[c]
                latest_date[c] = self.data['date'][i]
                if date_gap >= self.date_range:
                    sum_capacity[c] = 1
                    tmp[c] = [0] * self.date_range.days
                    tmp[c][0] = 1
                    count += 1
                else:
                    t = [0] * date_gap.days + tmp[c][0:self.date_range.days - date_gap.days]
                    t[0] += 1
                    sum_c = sum(t)
                    if sum_c <= self.capacity:
                        tmp[c] = t
                        sum_capacity[c] = sum_c
                        count += 1
                        self.labels_[i] = c + 1
        return count,

    def draw_result(self):
        self.draw_data()
        # self.draw_range()
        print(Counter(self.labels_))
        # plt.show()

    def draw_range(self):
        pass
        # plt.scatter(self.cluster_centers_[:, 0], self.cluster_centers_[:, 1], s=50)

    def draw_data(self):
        tmp = [20 if self.labels_[i] != 0 else 1 for i in range(len(self.labels_))]
        # plt.scatter(self.data['x'], self.data['y'], s = tmp, c = self.labels_)

        # plt.scatter(self.data['x'], self.data['y'], s=tmp, c=self.result)

    def draw_raw_data(self):
        pass
        # plt.scatter(self.data['x'],self.data['y'],s=1)
        # plt.show()


    def save_result(self):
        pass
        # data = pd.DataFrame({'id': self.data['傳染病報告單電腦編號'],
                                  # 'x': self.data['x'],
                                  # 'y': self.data['y'],
                                  # 'class':self.labels_})
        # data.to_csv("result.csv")
e = Evaluater("data.tsv", 5, 0.02, 200000, 3)
