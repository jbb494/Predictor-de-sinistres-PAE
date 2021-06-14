
import csv

threshold = 0.4
with open('../../Data/encargos_normalized.csv', 'r') as f:
    r = csv.reader(f)
    with open('../../Data/encargos_normalized_filtered.csv', 'w') as f2:
        l = list(r)
        f2.write(','.join(l[0]) + '\n')
        a = map(lambda x: [x[0], x[1], str(0) if float(x[2]) < threshold else str(x[2])], l[1:])
        f2.write('\n'.join(list(map(lambda x: ','.join(x), list(a)))))

