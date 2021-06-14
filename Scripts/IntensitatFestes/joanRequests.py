import requests
from bs4 import BeautifulSoup
import time
import re
import json
from functools import reduce
import random

getFirstNumber = lambda s: re.sub(r'[^0-9\s.]', '', s).split()[0].replace('.', '')

headers = {
    "authority":"www.google.com",
    "method":"GET",
    "scheme":"https",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"es-ES,es;q=0.9",
    "cache-control":"max-age=0",
    "cookie":"CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+ES.es+20150628-20-0; OTZ=5945116_48_52_123900_48_436380; SID=8wegpL0hPFO7m0-iEGDnIYmUHHd8nnmJhBES8m5HzKIzRTRGcg37Q11jqPG7Ueb__1K4ow.; __Secure-3PSID=8wegpL0hPFO7m0-iEGDnIYmUHHd8nnmJhBES8m5HzKIzRTRGaFiD4ihxIuW09VbWtcumPA.; HSID=A1TDZB_nImuYY2jhb; SSID=AWkMqoYuDrtg2kdC_; APISID=JfNhrttWFAz4GQ9p/AK9eAPE4Fq8G9b4Vg; SAPISID=6S9NZdTs_X95WzcM/AFlABBFPUxu06Jfqp; __Secure-3PAPISID=6S9NZdTs_X95WzcM/AFlABBFPUxu06Jfqp; SEARCH_SAMESITE=CgQItpIB; OGPC=19022519-1:; NID=214=IQA4dwtV1-UqSd5PAlKP6hVvS0wl5di8OdXxKmZQ1z9VarKdaeMDkROMFtGcG8ur0X5kd2mMLNJ4lKQ-UaQnuV_Iz1K9qShcX-sFO9oGubL-RxQ8Voixa_f3Dq0VuF9uu_BvGnA56ky1eSGRERLnhNwuZyHJW1LRsoRzRTVs8aOPnv9lZ7bgCry3jUPGpVdo0qYdx1igcpx0GNui-q3n0m_ucoNfT9y5p1jdQwyM1mrl1F3rKMthnqsCYhGWFI-JQ_qypGiLanikOCqc44k8tMcNoxKgx41koFY8MC0BmxnS8sg5nhotVvFOLaADDOISnxM0OHzu-78jYjI5ZPWC4FXJ3G1paWhpV8qjt-N1dyhvbdsBZAtVFdp95uEj2_8ko1FbFyE00rEAAslGobKxsP3ZxTwL-ZGWl80UeEBhA78; 1P_JAR=2021-04-29-20; DV=Y_l-XkO_Rrx5cBeTcarDqyE-UKL1kZdw4P5MyRCtAwAAADBkvrWJBdXBJAAAAND_N7s5Ubd7VwAAACZXk6Owkfa-fj0IgFHE6s4B_coMYA8CgIjjJVKBVqZx2IMAAA; SIDCC=AJi4QfGj2ViemcAygji6XNtYhV5u6vph_yPQ7j3knL_rftf2Rjb_UHRr9E0MGgO6uR44bn6oSR6I; __Secure-3PSIDCC=AJi4QfHQRyecdiSwHb03wkx3H54TbnAzhzBh9UyT5FSTaBxlOyfBHJN-iDJyjK03QyrjOoqEvwQ",
    "sec-ch-ua-mobile":"?0",
    "sec-fetch-dest":"document",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"same-origin",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "x-client-data":"CJG2yQEIprbJAQjEtskBCKmdygEIlqzKAQj4x8oBCPzsygEI5JzLAQioncsBCKKgywEY4ZrLARiOnssB",
}

def getIntensity(query: str):
    print(query)
    url = f"https://www.google.com/search?q={query}&cr=countryES"
    r = requests.get(url=url, headers=headers)
    try:
        b = BeautifulSoup(r.content)
        res = b.find(id="result-stats").text
        val = getFirstNumber(res)
    except Exception as e:
        with open('errors.log', 'w') as f2:
            f2.write(f"Query: {query} doesn't have views")
        val = 0
    time.sleep(0.7 + random.randint(0, 1000) / 1000.)
    return val

def main():
    with open('festes.json') as f:
        d = json.load(f)
        transform = lambda l: reduce(lambda acc, elem: {**acc, elem[1]: int(getIntensity(elem[0])) if elem[1] not in acc else acc[elem[1]] + int(getIntensity(elem[0]))}, l, {})
        final_dict = {elem: transform(d[elem]) for elem in d}
        json_str = json.dumps(final_dict, ensure_ascii=False)
        with open('intensitatsFestes.json', 'wb') as f2:
            f2.write(json_str.encode('UTF-8'))


if __name__ == '__main__':
    #main()
    print(getIntensity("la merce"))