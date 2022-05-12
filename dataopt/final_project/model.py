from scipy.stats import norm
import numpy as np
from desdeo_problem import variable_builder, ScalarObjective, MOProblem
import pandas as pd
from pymoo.core.problem import Problem

def get_markowitz(df: pd.DataFrame, w0):
    """
    Construct portfolio optimization problem
    based on historical data in dataframe
    and initial weights for assets
    """
    n = len(w0)
    variables = variable_builder(df.columns, w0, np.zeros(n), np.ones(n))
    change = df.pct_change()

    means = change.mean(axis=0)
    cov = change.cov().to_numpy()

    def f1(W):
        """
        Expected return
        """
        return W @ means
    
    def f2(W):
        """
        Risk
        """
        return np.array([(w.T @ cov @ w) for w in W])

    expected_return_f = ScalarObjective("expected return", f1, maximize=True)
    risk_f = ScalarObjective("risk", f2)

    prob = MOProblem(objectives = [expected_return_f, risk_f], variables=variables)

    return prob

class PortfolioSelection(Problem):
    def __init__(self, df, w0):
        n = len(w0)
        xl = np.zeros(n)
        xu = np.ones(n)
        super().__init__(n, 2, 0, xl, xu)
    
        change = df.pct_change()

        self.means = change.mean(axis=0)
        self.cov = change.cov().to_numpy()
        
    def _evaluate(self, x, out, *args, **kwargs):
        expected_return = x @ self.means
        risk = np.array([(w.T @ self.cov @ w) for w in x])
        out["F"] = np.array([-expected_return, risk]).T

# import data
# df = data.get_data_df()
# w0 = np.array([0.25, 0.25, 0.25, 0.25])
# problem = PortfolioSelection(df, w0)
# print(problem.evaluate(np.array([[0.25, 0.25, 0.25, 0.25], [0.20, 0.20, 0.20, 0.4]])))