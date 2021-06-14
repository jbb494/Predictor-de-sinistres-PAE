import csv

def filterCPCategorical():
    with open('../../OnlineData/CategoricalVolume.csv') as f:
        r = csv.reader(f)
        fList = list(r)
        with open('../../OnlineData/CategoricalVolume80.csv','w') as f2:
            f2.write(f"{','.join(fList[0])}\n")
            for row in fList[1:]:
                cp = str(row[1])
                if cp == "8001":
                    f2.write(f"{','.join(row)}\n")


def filterCleanCPs():
    right_CPs = ['8001', '8007', '8028', '8380', '8529', '17480', '43006', '43700']
    with open('../../OnlineData/clean_data_v2.csv') as f:
        r = list(csv.reader(f))
        with open('../../OnlineData/clean_data_v3.csv', 'w') as f2:
            f2.write(f"{','.join(r[0])}\n")
            for row in r[1:]:
                cp = row[1]
                if cp in right_CPs:
                    f2.write(f"{','.join(row)}\n")


def replaceChars():
    with open('../../OnlineData/clean_data_v3.csv') as f:
        r = list(csv.reader(f, delimiter=';'))
        with open('../../OnlineData/clean_data_v4.csv', 'w') as f2:
            f2.write(f"{','.join(r[0])}\n")
            for row in r[1:]:
                newRow = list(map(lambda x: x.replace(',','.'), row))
                f2.write(f"{','.join(newRow)}\n")


def main():
    replaceChars()

if __name__ == "__main__":
    main()