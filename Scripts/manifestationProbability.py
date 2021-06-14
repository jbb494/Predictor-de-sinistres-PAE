import numpy as np
import pandas as pd
import math

def readGoogleTrends(dates):
    # Actualment implementat per 2017
    csvFiles = ['../Data/Manifestacions2017.csv', '../Data/Manifestacions2018.csv', '../Data/Manifestacions2019.csv']
    nDays = len(dates)
    lvlArray = [0 for i in range(nDays)]

    for n in range(len(csvFiles)):
        mani = pd.read_csv(csvFiles[n])
        nWeeks = len(mani)
        # lvlArray: Una entrada per cada dia de l'any amb Pm

        for i in range(nWeeks):
            day = pd.Timestamp(mani.iloc[i].name).dayofyear
            lvl = mani.iloc[i][0]
            for j in range(5):
                actDay = day+j
                actN = n+1
                if actDay > 365:
                    actDay = actDay%365
                    n += 1
                    if n > 3:
                        break
                index = actDay * actN - 1
                lvlArray[index] += float(lvl) * math.exp(-j/2)

        # print(lvlArray)

    lvlArray = list(map(lambda x: round(x,2), lvlArray))

    matrix = pd.DataFrame(data=lvlArray, index=dates, columns=['Pm'])
    matrix.to_csv('../Data/Pm.csv')


if __name__ == "__main__":
    dates = pd.date_range(start='1/1/2017', end='1/1/2020', closed='left', freq='1D')
    readGoogleTrends(dates)
