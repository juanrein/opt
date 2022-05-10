from scipy.stats import norm
import numpy as np

def expectedReturn(X, w):
    """
    Compute expected return for each stock with given weights
    Params:
        X: ndarray(n weeks, n stocks) stock prices
        w: ndarray(n stocks,) weight for each stock
    """
    n,m = X.shape
    Ror = np.zeros((n-1,m))
    for i in range(len(X)-1):
        Ror[i] = (X[i+1] - X[i]) / X[i]
    means = Ror.mean(axis=0)
    vars = Ror.std(axis=0)
    #probability for each value
    Xp = np.array([norm.pdf(x, loc=m, scale=v) for x,m,v in zip(Ror.T, means, vars)])
    Xptotal = Xp.sum(axis=1)
    Xpw = Xptotal.dot(w)
    return Xpw


if __name__ == "__main__":
    import data
    X = data.get_data()
    print(X.shape)
    #equal weights
    w = np.array([0.25, 0.25, 0.25, 0.25])
    er = expectedReturn(X,w)
    print(er)