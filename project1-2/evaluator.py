# import pandas as pd
import datetime as dt
# import matplotlib.pyplot as plt
import csv
from random import random

class Hospital(object):
    def __init__(self, name, x, y, min_capacity, max_capacity):
        self.x = x
        self.y = y
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity

class Evaluater(object):
    def __init__(self, filename, dist, total_capacity, date_range, default_max_capacity, extend_capacity_list):
        self.dist = dist
        self.total_capacity = total_capacity
        self.date_range = dt.timedelta(date_range)
        self.extend_num = len(extend_capacity_list)

        self.data = self.resolve_data_points(filename)
        self.default_max_capacity = default_max_capacity
        self.extend_capacity_list = extend_capacity_list
        self.hospital = self.resolve_hospital("hospital.tsv")

        # self.nearest_hospital = self.calc_nearest_hospital(self.data, self.hospital)
        self.labels_ = [0 for i in range(len(self.data['x']))]
        self.k_hospitals = len(self.hospital)
        self.serve_total = [0] * self.k_hospitals

        # data range
        self.xmin = min(self.data['x'])
        self.xmax = max(self.data['x'])
        self.ymin = min(self.data['y'])
        self.ymax = max(self.data['y'])

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
            if not self.default_max_capacity:
                dc = int(row[3])
            else:
                dc = self.default_max_capacity
            h_list.append(Hospital(row[0], float(row[2]), float(row[1]), 0, dc))

        for i in self.extend_capacity_list:
            h_list.append(Hospital("Tmp", -1, -1, 0, i))

        return h_list

    def calc_nearest_hospital(self, data, hospital):
        nearest = [0] * len(data['x'])
        for i, p1 in enumerate(zip(self.data['x'], self.data['y'])):
            min_dist = 100000
            for j, hos in enumerate(hospital):
                dist = self.distance(p1, (hos.x, hos.y))
                if dist < min_dist and dist < self.dist:
                    min_dist = dist
                    nearest[i] = j + 1
        return nearest

    def nearest(self, i, p, ind):
        alpha = 1
        beta = 1
        hospital_pos_list = [(self.hospital[j].x, self.hospital[j].y) for j in range(self.k_hospitals - len(self.extend_capacity_list))]
        hospital_pos_list += ind[1]
        dist_list = [0] * self.k_hospitals
        s = 0
        for j in range(self.k_hospitals):
            d = self.distance(p, hospital_pos_list[j])
            if 0 < d <= self.dist and ind[0][j] > 0:
                dist_list[j] = d
                s += ind[0][j] ** alpha / dist_list[j] ** beta
            elif d == 0:
                return j + 1
            else:
                dist_list[j] = -1.

        p = 0
        r = random()
        for j, hos in enumerate(self.hospital):
            if dist_list[j] != -1.:
                p += ind[0][j] ** alpha / dist_list[j] ** beta / s
                if r < p:
                    return j + 1
        return 0

    def eval(self, ind):
        count = 0
        latest_date = [dt.datetime(1990, 1, 1)] * self.k_hospitals
        sum_capacity = [0] * self.k_hospitals
        tmp = [[0] * self.date_range.days for i in range(self.k_hospitals)]
        for i, p1 in enumerate(zip(self.data['x'], self.data['y'])):
            c = self.nearest(i, p1, ind)
            if c != 0:
                c -= 1
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
                    if sum_c <= ind[0][c]:
                        tmp[c] = t
                        sum_capacity[c] = sum_c
                        count += 1
        return count,


    def find_data_nearest_to(self, i, p, ind):
        return self.nearest_hospital[i]

    def distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def calc_labels(self, ind):
        count = 0
        latest_date = [dt.datetime(1990, 1, 1)] * self.k_hospitals
        sum_capacity = [0] * self.k_hospitals
        tmp = [[0] * self.date_range.days for i in range(self.k_hospitals)]
        for i, p1 in enumerate(zip(self.data['x'], self.data['y'])):
            c = self.nearest(i, p1, ind)
            if c != 0:
                c -= 1
                date_gap = self.data['date'][i] - latest_date[c]
                latest_date[c] = self.data['date'][i]
                if date_gap >= self.date_range:
                    sum_capacity[c] = 1
                    tmp[c] = [0] * self.date_range.days
                    tmp[c][0] = 1
                    count += 1
                    self.serve_total[c] += 1
                    self.labels_[i] = c + 1
                else:
                    t = [0] * date_gap.days + tmp[c][0:self.date_range.days - date_gap.days]
                    t[0] += 1
                    sum_c = sum(t)
                    if sum_c <= ind[0][c]:
                        tmp[c] = t
                        sum_capacity[c] = sum_c
                        count += 1
                        self.serve_total[c] += 1
                        self.labels_[i] = c + 1
        return count,

    def save_result(self, ind):
        # save data result
        data = self.data
        d = [[data['x'][i], data['y'][i], self.labels_[i]] for i in range(len(data['x']))]
        f = open("data_result.csv","w")
        w = csv.writer(f)
        w.writerows(d)
        f.close()
        # save hospital result
        hos = self.hospital
        h = [[hos[i].x, hos[i].y, 1] for i in range(len(hos))]
        j = 0
        for i in range(len(h)):
            if h[i][0] == -1:
                h[i][0] = ind[1][j][0]
                h[i][1] = ind[1][j][1]
                h[i][2] = 0
                j += 1
        f = open("hospital_result.csv","w")
        w = csv.writer(f)
        w.writerows(h)
        f.close()
        print(self.serve_total)
        pass
        # data = pd.DataFrame({'id': self.data['傳染病報告單電腦編號'],
                                  # 'x': self.data['x'],
                                  # 'y': self.data['y'],
                                  # 'class':self.labels_})
        # data.to_csv("result.csv")

    def plot_raw(self, extend_list):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(self.data['x'], self.data['y'], s=1)
        for i in self.hospital:
            ax1.scatter(i.x, i.y, s=20, c='r')

        for i in extend_list:
            ax1.scatter(i[0], i[1], s=20, c='g')
        plt.show()

if __name__ == "__main__":
    e = Evaluater("sorted.tsv", dist=0.02, total_capacity=800, date_range=3, default_max_capacity=150, extend_capacity_list=[20] * 3)
    e.plot_raw()
    pass
