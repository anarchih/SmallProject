import matplotlib.pyplot as plt
import csv

# draw data
data = {'x': [], 'y': [], 'class':[]}
f = open("data_result.csv")
for row in csv.reader(f):
    data['x'].append(float(row[0]))
    data['y'].append(float(row[1]))
    data['class'].append(int(row[2]))

size = [15 if data['class'][i] != 0 else 1 for i in range(len(data['x']))]
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(data['x'], data['y'], s=size, c=data['class'])


# draw hospital

hos = {'x': [], 'y': []}
f = open("hospital_result.csv")
for row in csv.reader(f):
    if row[2] == '1':
        ax1.scatter(float(row[0]), float(row[1]), s=35, c='r')
    else:
        ax1.scatter(float(row[0]), float(row[1]), s=35, c='c')


plt.show()
