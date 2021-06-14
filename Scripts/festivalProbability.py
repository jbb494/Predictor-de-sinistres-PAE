import pandas as pd
import math

def main():
    originaldf = pd.read_csv(filepath_or_buffer='../Data/FestivalsProbability.csv', sep=',', skip_blank_lines=False, index_col=0, header=0, names=['Pf'])
    df = originaldf.sort_index()
    dates = pd.date_range(start='1/1/2017', end='1/1/2020', closed='left', freq='1D')

    nDays = len(dates)
    lvlArray = [0 for i in range(nDays)]
    yearMod = {'2017':1, '2018':2, '2019': 3}

    for i in range(len(df)):
        pdT = pd.Timestamp(df.iloc[i].name)
        day = pdT.dayofyear
        lvl = df.iloc[i][0]
        for j in range(5):
            actDay = day + j
            actN = yearMod[str(pdT.year)]
            if actDay > 365:
                actDay = actDay%365
                actN += 1
                if actN > 3:
                    break
            index = actDay * actN - 1
            lvlArray[index] += float(lvl) * math.exp(-j/2)


    lvlArray = list(map(lambda x: round(x,2), lvlArray))

    matrix = pd.DataFrame(data=lvlArray, index=dates, columns=['Pf'])
    matrix.to_csv('../Data/Pf.csv')

if __name__ == "__main__":
    main()