import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
from pmdarima.arima import auto_arima

x = 1.0 + 0.5 * np.sin(np.linspace(0, 10 * 2 * np.pi, 100))
x = x + 0.01 * np.arange(len(x)) #upwards trend
noise = np.random.normal(0, 0.1, size=x.shape)
noisyx = x + noise
i = pd.date_range("1/1/2020", periods=len(noisyx), freq="W")
prices = pd.Series(noisyx[:90], index=i[:90])
pricesFuture = pd.Series(x[90:], index=i[90:])
# mod = ARIMA(prices, order=(3,0,1)).fit()
# pricesForecast = mod.predict(len(prices), len(noisyx)-1)
arima = auto_arima(prices, start_p=1, max_p=5, start_d=1,
                   max_d=5, start_q=1, max_q=5)
print(arima.get_params())
pricesForecast = arima.predict(len(pricesFuture))
pricesForecast = pd.Series(pricesForecast, index = pricesFuture.index)
print(mean_absolute_error(pricesFuture, pricesForecast))

plt.plot(prices)
plt.plot(pricesForecast)
plt.plot(pricesFuture)
plt.show()
