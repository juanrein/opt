from urllib.request import urlopen, Request
from typing import TextIO
import csv
import pandas as pd
from pathlib import Path
import os

stocks = ["SIE.DE", "ADS.DE", "AIR.PA", "KNEBV.HE"]
urlTemplate = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1620582946&period2=1652118946&interval=1wk&events=history&includeAdjustedClose=true"

dataDir = Path("./data")
for child in dataDir.iterdir():
    os.remove(child)

#  0     1    2    3   4    5          6
#b'Date,Open,High,Low,Close,Adj Close,Volume\n'
for stockName in stocks:
    url = urlTemplate.format(stockName)
    with urlopen(url) as result:
        s = result.readlines()
        fileName = stockName.replace(".", "")
        with open(f"./data/{fileName}.csv", mode="xb") as outputFile:
            outputFile.writelines(s)