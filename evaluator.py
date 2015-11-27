import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from collections import Counter


class Cluster(object):
    def __init__(self, capacity):
        self.week = [0] * 60

class Evaluater(object):
    def __init__(self, filename, k, dist, capacity):
        self.data = self.read_tsv(filename)
        self.k = k
        self.dist = dist
        self.cluster = Cluster(capacity)
        self.xmin = self.data.x.min()
        self.ymin = self.data.y.min()
        self.xmax = self.data.x.max()
        self.ymax = self.data.y.max()
        self.labels_ = [0 for i in range(len(self.data))]

    def read_tsv(self, filename):
        data = pd.read_csv(filename, sep="\t")
        # rows = random.sample(list(data.index), 5000)
        # data = data.ix[rows]
        data = data.rename(columns = {'經度座標':'x'})
        data = data.rename(columns = {'緯度座標':'y'})

        dtime = pd.DataFrame([[dt.datetime.strptime('2015/' + i, "%Y/%m/%d")] for i in data['發病日期']], columns=['date'])
        data = data.join(dtime)
        del data['發病日期']
        return data

    def evaluate(self, ind):
        count = 0
        for p1 in zip(self.data.x, self.data.y):
            for j, p2 in enumerate(ind):
                if self.distance(p1, p2) < self.dist:
                    count += 1
                    break
        return count,

    def distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def calc_labels(self, ind):
        for i, p1 in enumerate(zip(self.data.x, self.data.y)):
            Min = 10000
            for j, p2 in enumerate(ind, 1):
                dist = self.distance(p1, p2)
                if dist < self.dist and dist < Min:
                    Min = dist
                    self.labels_[i] = j


    def draw_result(self):
        self.draw_data()
        # self.draw_range()
        print(Counter(self.labels_))
        plt.show()

    def draw_range(self):
        pass
        # plt.scatter(self.cluster_centers_[:, 0], self.cluster_centers_[:, 1], s=50)

    def draw_data(self):
        tmp = [20 if self.labels_[i] != 0 else 1 for i in range(len(self.labels_))]
        plt.scatter(self.data.x, self.data.y, s = tmp, c = self.labels_)

        # plt.scatter(self.data.x, self.data.y, s=tmp, c=self.result)

    def draw_raw_data(self):
        plt.scatter(self.data.x,self.data.y,s=1)
        plt.show()


    def save_result(self):
        data = pd.DataFrame({'id': self.data['傳染病報告單電腦編號'],
                                  'x': self.data.x,
                                  'y': self.data.y,
                                  'class':self.labels_})
        data.to_csv("result.csv")
# e = Evaluater("data.tsv", 5, 200000, 0.02)
