import csv
import matplotlib.pyplot as plt



with open('../encargos.csv') as f:
    r = csv.reader(f)
    col = 5
    first = True
    freq = {}
    for row in r:
        if first:
            first = False
            continue
        if row[0].split("-")[0] == "2017":
            month = row[0].split("-")[1]
            if month in freq:
                freq[month] += int(row[col])
            else:
                freq[month] = int(row[col])

    freq = dict(sorted(freq.items()))

    x = freq.keys()
    y = freq.values()

    plt.title(f"Year: 2017, Postal: -- ")
    plt.plot(x, y)
    labels = list(map(lambda x: f'0{x}-2017', range(1, 10))) + list(map(lambda x: f'{x}-2017', range(10, 13)))
    print(labels)
    # plt.xticks(x, labels, rotation='vertical')
    plt.show()






