import csv
import pandas as pd
import numpy as np


def categoricalThreshold(value):
    if value < 1:
        return '0'
    elif value < 2.0:
        return '1'
    elif value < 3.5:
        return '2'
    elif value < 6.5:
        return '3'
    else:
        return '4'

def binaryThreshold(value):
    if value <= 1:
        return '0'
    else:
        return '1'

def categorize():
    with open('../../OnlineData/FinalDataFinal.csv') as f:
        with open('../../OnlineData/CategoricalVolume_8cpFinalBinary.csv', 'w') as fw:
            r = list(csv.reader(f))
            fw.write(f"{','.join(r[0])}\n")
            for row in r[1:]:
                newRow = row
                row[20:] = list(map(lambda x: binaryThreshold(float(x)), row[20:])) # S'ha de fer absolut
                fw.write(f"{','.join(newRow)}\n")


def unNormalize():
    finalData = pd.read_csv('../../OnlineData/Final_data.csv', index_col=0)
    encargos = pd.read_csv('../../Data/encargos.csv', index_col=0)

    with open('../../OnlineData/Final_data.csv') as finalData:
        with open('../../OnlineData/Final_data_NoFilter.csv', 'w') as fw:
            dataList = list(csv.reader(finalData))
            fw.write(f"{','.join(dataList[0])}\n")
            for row in dataList[1:]:
                d, cp = row[:2]
                auxEncargos = encargos.loc[encargos['DesCPOcurrencia'] == float(cp)]
                newRow = row
                try:
                    newRow[-1] = str(auxEncargos.loc[d, 'NumEncargos'])
                except:
                    pass

                fw.write(f"{','.join(newRow)}\n")


def main():
    categorize()


if __name__ == "__main__":
    main()