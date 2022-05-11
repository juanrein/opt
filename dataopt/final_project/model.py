from scipy.stats import norm
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt

def expected_return(X, w):
    n, m = X.shape
    Ror = np.zeros((n-1, m))
    for i in range(len(X)-1):
        Ror[i] = (X[i+1] - X[i]) / X[i]
    means = Ror.mean(axis=0)
    return np.dot(w, means) * 52

def risk(X, w):
    n, m = X.shape
    Ror = np.zeros((n-1, m))
    for i in range(len(X)-1):
        Ror[i] = (X[i+1] - X[i]) / X[i]
    cov = np.cov(Ror.T)
    return (w.T @ cov @ w)


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


