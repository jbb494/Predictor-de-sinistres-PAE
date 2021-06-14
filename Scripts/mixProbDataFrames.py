import pandas as pd

def main():
    pm = pd.read_csv(filepath_or_buffer='../Data/Pm.csv', sep=',', header=0, index_col=0)
    pf = pd.read_csv(filepath_or_buffer='../Data/Pf.csv', sep=',', header=0, index_col=0)

    frames = pf['Pf'].values
    dataset = pm.assign(Pf=frames)

    dataset.to_csv('../Data/Probabilities.csv')

if __name__ == "__main__":
    main()

