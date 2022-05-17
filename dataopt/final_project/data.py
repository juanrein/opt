from urllib.request import urlopen
import pandas as pd
import os
from datetime import datetime


URLTEMPLATE = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1wk&events=history&includeAdjustedClose=true"
STOCKNAMES = [
    "ADS.DE",
    "ADYEN.AS",
    "AD.AS",
    "AI.PA",
    "AIR.PA",
    "ALV.DE",
    "ABI.BR",
    "ASML.AS",
    "CS.PA",
    "CS.PA",
    "BAYN.DE",
    "BBVA.MC",
    "SAN.MC",
    "BMW.DE",
    "BNP.PA",
    "CRG.IR",
    "BN.PA",
    "DB1.DE",
    "DPW.DE",
    "DTE.DE",
    "ENEL.MI",
    "ENI.MI",
    "EL.PA",
    "FLTR.IR",
    "RMS.PA",
    "IBE.MC",
    "ITX.MC",
    "IFX.DE",
    "INGA.AS",
    "ISP.MI",
    "KER.PA",
    "KNEBV.HE",
    "OR.PA",
    "LIN.DE",
    "MC.PA",
    "MBG.DE",
    "MUV2.DE",
    "RI.PA",
    "PHIA.AS",
    "PRX.AS",
    "SAF.PA",
    "SAN.PA",
    "SAP.DE",
    "SU.PA",
    "SIE.DE",
    "STLA.MI",
    "TTE.PA",
    "DG.PA",
    "VOW.DE",
    "VNA.DE",
]
FILENAME = "./data/stock_prices.csv"
STARTDATE = int(datetime(2018, 1, 1).timestamp())
ENDDATE = int(datetime(2022, 1, 1).timestamp())

def fetch_stock_prices():
    """
    Read stock prices from yahoo finance 
    and write it to csv file
    """
    # remove existing file
    os.remove(FILENAME)

    data = None

    #  0     1    2    3   4    5          6
    #b'Date,Open,High,Low,Close,Adj Close,Volume\n'
    for stockName in STOCKNAMES:
        url = URLTEMPLATE.format(stockName, STARTDATE, ENDDATE)
        with urlopen(url) as result:
            stockdf = pd.read_csv(result, index_col=0)
        price = stockdf["Adj Close"].rename(stockName)
        if data is None:
            data = price
        else:
            data = pd.concat((data, price), axis=1)

    data.to_csv(FILENAME)

def get_data_df():
    """
    Get data as a pandas dataframe
    """
    return pd.read_csv(FILENAME, index_col=0, parse_dates=True)

# fetch_stock_prices()