import json
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getFestivalsDateName():
    res = {}
    with open('festes.json', encoding='utf-8') as json_file:
        data = dict(json.load(json_file))
        for month in data.keys():
            for fest, day in data[month]:
                actDay = f"{day}/{month}"
                if actDay not in res:
                    res[actDay] = [fest]
                else:
                    res[actDay].append(fest)

    return res


def main():
    path_chrome = "C:\\Program Files\\chromedriver.exe"

    festivalsDict = getFestivalsDateName()
    url = "https://www.google.com/search?q="
    driver = webdriver.Chrome(path_chrome)
    driver.maximize_window()

    dates = pd.date_range(start='1/1/2017', end='1/1/2020', closed='left', freq='1D')
    intensity = dict.fromkeys(dates, 0)    # {Date: NumSearchs}

    datesList = list(festivalsDict.keys())
    for i in range(120,147):
        date = datesList[i]
        festivals = festivalsDict[date]

        for fest in festivals:
                actURL = url + fest + " catalunya"
                driver.get(actURL)

                try:
                    element = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.ID, "result-stats")))
                except Exception as e:
                    print("Unexpected error: ", e)
                    print(f"Info per festa \"{fest}\" no ha sigut trobada")
                    continue

                results = driver.find_element_by_id("result-stats").text
                numResults = str(results).split()[1]

                for d in ["2017", "2018", "2019"]:
                    auxDate = pd.DataFrame({'year':[d], 'month':[date.split('/')[1]], 'day':[date.split('/')[0]]})
                    auxDate = pd.to_datetime(auxDate)[0]
                    value = int(numResults.replace(".",""))
                    intensity[auxDate] += value
                    with open("../../Data/FestivalsProbability.csv", 'a') as csv_file:
                        csv_file.write(f"{str(auxDate.date())},{value}\n")

                time.sleep(0.5 + random.randint(1,100)/100.0)

    driver.quit()
    #
    # matrix = pd.DataFrame(data=intensity.values(), index=dates, columns=['Pf'])
    # matrix.to_csv('../../Data/FestivalsProbability.csv')

if __name__ == "__main__":
    main()

