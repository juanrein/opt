import numpy as np
from pmdarima.arima import auto_arima

def computeReturn(df, predictionPeriod: int):
    """
    Predicts the change in prices of stocks predictionPeriod amounts of 
    steps into future
    """
    changes = []
    for stockName in df:
        x = df[stockName]
        # arima doesn't allow Nans
        x = x.fillna(method="backfill").fillna(method="ffill")
        
        arima = auto_arima(x, start_p=1, max_p=5, start_d=1,
        max_d=5, start_q=1, max_q=5, maxiter=100)
        pricesForecast = arima.predict(predictionPeriod)
        
        next = pricesForecast[-1]
        prev = x[-1]
        change = (next - prev) / prev
        changes.append(change)

    return np.array(changes)

