import csv
import pandas as pd
from functools import reduce
from datetime import date
from statistics import mean
from matplotlib import pyplot as plt
import numpy as np
import math


def main():
    column = 2
    years = ["2017", "2018", "2019"]

    get_number_of_days_in_month = lambda month, year: (date(year + math.floor(month/12), (month % 12) + 1, 1) - date(year, month, 1)).days

    # Initialize it for the whole 3 years
    mean_month_cp = {}
    with open('../../Data/encargos.csv') as f:
        r = csv.reader(f)
        l = list(r)
        for row in l[1:]:
            d, cp = row[:2]
            volume = list(map(float, row[2:]))
            year, month, day = d.split('-')
            if cp in mean_month_cp:
                if month in mean_month_cp[cp]:
                    for i in range(len(volume)):
                        mean_month_cp[cp][month][i] += [volume[i]]
                else:
                    mean_month_cp[cp][month] = {}
                    for i in range(len(volume)):
                        mean_month_cp[cp][month][i] = [volume[i]]
            else:
                mean_month_cp[cp] = {month: {}}
                for i in range(len(volume)):
                    mean_month_cp[cp][month][i] = [volume[i]]

        dateCP = {}     # {data: [cp]}
        availCP = set()  # {cp}
        with open('../../Data/testingNewData.csv', 'w') as n_f:
            n_f.write(f'{",".join(l[0])}\n')
            for row in l[1:]:
                d, cp = row[:2]
                volume = row[2:]

                auxDate = str(pd.Timestamp(d).date())
                dateCP[auxDate] = [cp] if auxDate not in dateCP else dateCP[auxDate] + [cp]
                if cp not in availCP:
                    availCP.add(cp)

                volume = list(map(float, volume))
                year, month, day = d.split('-')
                volume_final = volume
                for i in range(len(volume)):
                    volume_final[i] = (volume_final[i] - np.mean(mean_month_cp[cp][month][i])) / (np.std(mean_month_cp[cp][month][i]) + 1e-100)

                n_f.write(f'{str(pd.Timestamp(d).date())},{cp},{",".join(list(map(str,volume_final)))}\n')

            for d in dateCP.keys():
                usedCP = dateCP[d]
                notUsedCP = availCP.difference(set(usedCP))
                month = d.split('-')[1]
                for cp in notUsedCP:
                    if month in mean_month_cp[cp]:
                        n_f.write(f'{d},{cp}')
                        for i in range(len(volume)):
                            n_f.write(f',{- np.mean(mean_month_cp[cp][month][i]) / (np.std(mean_month_cp[cp][month][i]) + 1e-100)}')
                        n_f.write(f'\n')
                    else:
                        n_f.write(f'{d},{cp},{",".join(map(lambda x: str(float(x)) ,np.repeat(0, len(l[0])-2)))}\n')



if __name__ == "__main__":
    main()
