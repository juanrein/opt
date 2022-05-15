import numpy as np
from pymoo.core.problem import Problem


class PortfolioSelection(Problem):
    """
    Portfolio selection problem
    choose weight w_i for each asset n to
    maximize expected return 
    and minimize risk
    subject to
    0 <= wi <= 1
    sum(wi) = 1
    note: expected return is negated here so
          both objective can be minimized
    """

    def __init__(self, df, w0):
        n = len(w0)
        xl = np.zeros(n)
        xu = np.ones(n)
        super().__init__(n, 2, 0, xl, xu)

        change = df.pct_change()

        self.means = change.mean(axis=0)
        self.cov = change.cov()

    def _evaluate(self, W, out, *args, **kwargs):
        """
        return
            np.array([n, 2] (-expected return, risk)
        """
        expected_return = W @ self.means
        risk = np.array([(w.T @ self.cov @ w) for w in W])

        out["F"] = np.array([-expected_return, risk]).T


# import data
# df = data.get_data_df()
# w0 = np.array([0.25, 0.25, 0.25, 0.25])
# problem = PortfolioSelection(df, w0)
# print(problem.evaluate(np.array([[0.25, 0.25, 0.25, 0.25], [0.20, 0.20, 0.20, 0.4]])))
