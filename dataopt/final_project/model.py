from xml.dom.expatbuilder import parseFragmentString
import numpy as np
from pymoo.core.problem import Problem
from statsmodels.tsa.arima.model import ARIMA


class PortfolioSelection(Problem):
    """
    Portfolio selection problem
    choose weight w_i for each asset n to
    maximize expected return 
    and minimize risk
    subject to
        w_min <= wi <= w_max
        sum(wi) = 1
        Cardinality constraint
            there need to be between c_min and c_max stocks
            in the portfolio
    note: expected return is negated here so
          both objective can be minimized
    """

    def __init__(self, df, w_min, w_max, c_min, c_max, n_stocks):
        xl = np.concatenate((np.full(n_stocks, w_min), np.zeros(n_stocks, dtype=int)))
        xu = np.concatenate((np.full(n_stocks, w_max), np.ones(n_stocks, dtype=int)))

        super().__init__(2 * n_stocks, 2, 2, xl, xu)

        self.w_min = w_min
        self.w_max = w_max
        self.c_min = c_min
        self.c_max = c_max
        self.n_stocks = n_stocks

        change = df.pct_change()

        self.means = change.mean(axis=0)
        self.cov = change.cov()

    def _evaluate(self, X, out, *args, **kwargs):
        W = X[:, :self.n_stocks]
        Y = X[:, self.n_stocks:]
        WW = W * Y
        expected_return = WW @ self.means
        
        risk = np.array([(w.T @ self.cov @ w) for w in WW])

        n_stocks_in_portfolio = Y.sum(axis=1)
        #n_stocks in solution needs to be between c_min and c_max
        g1 = n_stocks_in_portfolio - self.c_max
        g2 = self.c_min - n_stocks_in_portfolio

        out["F"] = np.array([-expected_return, risk]).T
        out["G"] = np.array([g1, g2]).T

class PortfolioSelectionArima(Problem):
    """
    Portfolio selection problem
    choose weight w_i for each asset n to
    maximize expected return 
    and minimize risk
    subject to
    w_min <= wi <= w_max
    sum(wi) = 1
    Cardinality constraint
        there need to be between c_min and c_max stocks
        in the portfolio
    note: expected return is negated here so
          both objective can be minimized
    """
    def __init__(self, df, w0, w_min, w_max, c_min, c_max):
        n = len(w0)
        xl = np.full(n, w_min)
        xu = np.full(n, w_max)
        super().__init__(n, 2, 0, xl, xu)
        self.df = df
        self.w_min = w_min
        self.w_max = w_max
        self.c_min = c_min
        self.c_max = c_max

        change = df.pct_change()
        self.cov = change.cov()
        rors = []
        for c in df:
            x = df[c]
            arima = ARIMA(x, order=(2,1,2))
            res = arima.fit()
            x_hat = res.forecast(2)
            a = x_hat[0]
            b = x_hat[1]
            rors.append((b - a)/a)

        self.rors = np.array(rors)

    def _evaluate(self, W, out, *args, **kwargs):
        expected_return = W @ self.rors
        risk = np.array([(w.T @ self.cov @ w) for w in W])

        out["F"] = np.array([-expected_return, risk]).T

# import data
# df = data.get_data_df()
# w0 = np.array([0.25, 0.25, 0.25, 0.25])
# problem = PortfolioSelection(df, w0)
# print(problem.evaluate(np.array([[0.25, 0.25, 0.25, 0.25], [0.20, 0.20, 0.20, 0.4]])))
