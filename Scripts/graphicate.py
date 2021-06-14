import csv
from typing import List
from matplotlib import pyplot as plt
from functools import reduce

l: List = []
year = "2017"
postal = ""

with open('../encargos.csv') as f:
    r = csv.reader(f)
    for row in list(r)[1:]:
        l.append(list(row))

l = list(filter(lambda q: year in q[0], l))
l = list(filter(lambda q: postal == q[1] if postal else True, l))

l.sort(key=lambda x: x[0])

x, y = reduce(lambda acc, elem: [acc[0] + [elem[0]], acc[1] + [int(elem[2])]], l, [[], []])

#print(x[:30], y[:30])
plt.title(f"Year: {year}, Postal: {postal}")
plt.plot(x, y)
labels = list(map(lambda x: f'01-0{x}-{year}', range(1, 10))) + list(map(lambda x: f'01-{x}-{year}', range(10, 13)))
print(labels)
plt.xticks(x, labels, rotation='vertical')
plt.show()