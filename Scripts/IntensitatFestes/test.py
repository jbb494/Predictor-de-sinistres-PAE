import pandas as pd
import csv


x = pd.to_datetime("1-1-2017")

with open("../../basura2.csv", "w") as csv_file:
    csv_file.write(f"{str(x.date())},30 \n")