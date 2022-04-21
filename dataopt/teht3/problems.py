from sklearn.metrics import r2_score
import numpy as np
from pymoo.factory import get_problem, get_visualization
from scipy.stats import qmc
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from pymoo.core.problem import Problem
from scipy.stats import norm

class ExpectedImprovement(Problem):
    def __init__(self, p: Problem, model, fxb, xi = 1e-5):
        """
        p: problem object
        model: model object
        fxb: best objective function value found
        xi: a parameter controlling the degree of exploration
        """
        super().__init__(n_var=p.n_var, n_obj=1,
                         n_constr=0, xl=p.xl, xu=p.xu)
        self.model = model
        self.fxb = fxb
        self.xi = xi

    def _evaluate(self, X, out, *args, **kwargs):
        x_mean, x_std = self.model.predict(X, return_std=True)
        x_var = np.sqrt(x_std).reshape(-1, 1)
        # expected improvement
        inner = (self.fxb - x_mean - self.xi)/x_var
        left = (self.fxb - x_mean - self.xi) * norm.cdf(inner)
        right = x_var * norm.pdf(inner)
        EI = left + right
        # negate to fit the interface requiring minimization
        out["F"] = -EI

class Surrogate(Problem):
    """
    Surrogate to Problem wrapper
    """
    def __init__(self, p, model):
        """
        p: problem object
        model: surrogate model
        """
        super().__init__(n_var=p.n_var, n_obj=1,
                         n_constr=0, xl=p.xl, xu=p.xu)
        self.model = model

    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = self.model.predict(X)