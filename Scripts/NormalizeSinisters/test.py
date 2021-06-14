import csv

def main():
    with open('../../Data/encargos_normalized.csv') as f:
        r = csv.reader(f)
        sum = 0.0
        for row in list(r)[1:]:
            month = row[0].split('-')[1]
            cp = row[1]
            sum += float(row[2]) if month == '01' and cp == '08001' else 0.0

        print(sum)

if __name__ == "__main__":
    main()