import csv
from typing import List
from matplotlib import pyplot as plt
from functools import reduce

l: List = []
year = "2019"
month = "04"
postal = "17480"

col_label = 20
with open('../../Data/Final_data_8cp.csv') as f:
    r = csv.reader(f)
    for row in list(r)[1:]:
        l.append(list(row))

l = list(filter(lambda q: year in q[0].split('-')[0] and month in q[0].split('-')[1], l))
l = list(filter(lambda q: postal == q[1] if postal else True, l))

l.sort(key=lambda x: x[0])

plt.title(f"Any: {year}, Mes: {month}, Codi Postal: {postal}")
x, y = list(reduce(lambda acc, elem: [acc[0] + [elem[0].split('-')[2]], acc[1] + [float(elem[col_label])]], l, [[], []]))
print(sum(y))
plt.xticks(rotation='vertical')
plt.plot(x, y)
plt.savefig('../../Images/Experimentacio/RegresionExample.png')
plt.show()
