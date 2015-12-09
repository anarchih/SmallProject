# import pandas as pd
import datetime as dt
# import matplotlib.pyplot as plt
import csv

class Hospital(object):
    def __init__(self, name, x, y, min_capacity, max_capacity):
        self.x = x
        self.y = y
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity

class Evaluater(object):
    def __init__(self, filename, dist, total_capacity, date_range):
        self.data = self.resolve_data_points(filename)
        self.hospital = self.resolve_hospital("hospital.tsv")
        self.dist = dist
        self.total_capacity = total_capacity
        self.date_range = dt.timedelta(date_range)
        self.labels_ = [0 for i in range(len(self.data['x']))]
        self.k_hospitals = len(self.hospital)

    def resolve_data_points(self, filename):
        data = {'x': [], 'y': [], 'date':[]}
        f = open(filename, "r")
        f.readline()
        for row in csv.reader(f, delimiter='\t'):
            data['x'].append(float(row[9]))
            data['y'].append(float(row[10]))
            data['date'].append(dt.datetime.strptime('2015/' + row[5], "%Y/%m/%d"))
        return data

    def resolve_hospital(self, filename):
        h_list = []
        f = open(filename, "r")
        f.readline()
        for row in csv.reader(f, delimiter='\t'):
            h_list.append(Hospital(row[0], row[1], row[2], 0, 1000))
        return h_list

    def eval(self, ind):
        return 1,

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

    def save_result(self):
        pass
        # data = pd.DataFrame({'id': self.data['傳染病報告單電腦編號'],
                                  # 'x': self.data['x'],
                                  # 'y': self.data['y'],
                                  # 'class':self.labels_})
        # data.to_csv("result.csv")


if __name__ == "__main__":
    pass
