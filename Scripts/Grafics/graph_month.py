import csv
from typing import List
from matplotlib import pyplot as plt
from functools import reduce

l: List = []
year = "2017"
postal = ""

with open('../../Data/encargos.csv') as f:
    r = csv.reader(f)
    for row in list(r)[1:]:
        l.append(list(row))

l = list(filter(lambda q: year in q[0], l))
l = list(filter(lambda q: postal == q[1] if postal else True, l))

l.sort(key=lambda x: x[0])

dict_graph = reduce(lambda acc, elem:
                    {**acc,
                     elem[0].split('-')[1]: float(elem[2]) +
                                            (acc[elem[0].split('-')[1]]
                                            if elem[0].split('-')[1] in acc else 0)
                     },
            l, {})
print(dict_graph)
plt.title(f"Year: {year}, Postal: {postal}")
plt.plot(list(dict_graph.keys()), list(dict_graph.values()))
plt.show()
