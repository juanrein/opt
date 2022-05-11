from scipy.stats import norm
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt
from desdeo_problem import variable_builder, ScalarObjective, MOProblem, VectorObjective
import pandas as pd


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
        return W @ means
    
    def f2(W):
        return np.array([(w.T @ cov @ w) for w in W])

    expected_return_f = ScalarObjective("expected return", f1, maximize=True)
    risk_f = ScalarObjective("risk", f2)

    prob = MOProblem(objectives = [expected_return_f, risk_f], variables=variables)

    return prob

def createWeightVectors(M, H):
    """
    Creates evenly distributed weight vectors
    in M dimensional space with H fractions 
    """
    # 0/H,1/H,...H/H
    fractions = np.linspace(0, 1, H+1)
    N = math.comb(H+M-1, M-1)
    U = np.zeros((N, M))
    ui = 0
    # iterate possible fraction sets and pick those that
    # add up to 1
    for u in itertools.product(fractions, repeat=M):
        if math.isclose(sum(u), 1.0):
            U[ui] = np.array(u)
            ui += 1
    return U

