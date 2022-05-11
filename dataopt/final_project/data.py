from urllib.request import urlopen, Request
from typing import TextIO
import csv
import pandas as pd
from pathlib import Path
import os
import numpy as np

def fetch_stock_prices():
    """
    Read stock data from yahoo finance 
    and write it to csv files in data folder
    """
    stocks = ["SIE.DE", "ADS.DE", "AIR.PA", "KNEBV.HE"]
    urlTemplate = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1620582946&period2=1652118946&interval=1wk&events=history&includeAdjustedClose=true"

    #remove existing files
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

def get_data():
    """
    Get stock prices as an array
    """
    dataDir = Path("./data")
    X = []
    for child in dataDir.iterdir():
        df = pd.read_csv(child)
        #maybe use adjusted close
        x = df.get("Close").interpolate().to_numpy()
        X.append(x)
    #pandas.concatenate?
    return np.array(X).T

def get_data_df():
    return pd.read_csv("./data/stock_prices.csv", index_col=0)

def mergeCsvs():
    """
    Combines all csv into one containing all the stocks
    """
    dataDir = Path("./data")
    data = None
    #add each stock as its own column to dataframe
    for child in dataDir.iterdir():
        if child.name == "stock_prices.csv":
            continue
        stockdf = pd.read_csv(child)
        x = pd.DataFrame(stockdf["Adj Close"].to_numpy(), columns=[child.name])
        if data is None:
            data = x
        else:
            data = pd.concat((data, x), axis=1)

    data.to_csv("./data/stock_prices.csv")
