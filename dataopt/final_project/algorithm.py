import itertools
import math
import numpy as np
from pymoo.core.repair import Repair
from pymoo.core.population import Population
from sklearn.utils import indices_to_mask




class OneSumRepair(Repair):
    def __init__(self, w_min, w_max, n_stocks) -> None:
        super().__init__()
        self.w_min = w_min
        self.w_max = w_max
        self.n_stocks = n_stocks

    def _do(self, problem, pop: Population, **kwargs):
        """
        Transforms weight vectors into feasible ones
        so that for each row the sum is 1
        Kaucic, M., Moradi, M., & Mirzazadeh, M. (2019). 
        Portfolio optimization by improved NSGA-II and SPEA 2 based on different risk measures. 
        Financial Innovation, 5(1), 1-28.
        """
        X = pop.get("X")
        W = X[:, :self.n_stocks]
        Y = X[:, self.n_stocks:]

        Wminmax = W.clip(self.w_min, self.w_max)
        #set weights of stocks that are not selected to zero
        Wminmax = W * Y
        Wsum = Wminmax.sum(axis=1)
        Wnorm = Wminmax.T / Wsum

        #Wsum can be zero if none stocks are chosen
        nanValue = 1/self.n_stocks
        Wnorm = np.nan_to_num(Wnorm, nan=nanValue)

        WnormY = np.hstack((Wnorm.T, Y))
        pop.set("X", WnormY)
        return pop

def createInitialPopulation(population_size, n_stocks):
    W = np.random.random((population_size,n_stocks))
    Y = np.random.randint(0, 2, size=(population_size, n_stocks))
    P = Population.create(np.hstack((W, Y)))
    Pr = OneSumRepair(n_stocks).do(None, P)
    return Pr

class BoundedRepair(Repair):
    def __init__(self, w_min, w_max, c_min, c_max, n_stocks) -> None:
        super().__init__()
        self.w_min = w_min
        self.w_max = w_max
        self.c_min = c_min
        self.c_max = c_max
        self.n_stocks = n_stocks

    def _do(self, problem, pop, **kwargs):
        """
        Transforms weight vectors into feasible ones
        so that for each row the sum is 1
        and each individual weight is between
        w_min and w_max

        Quintana, D., Denysiuk, R., Garcia-Rodriguez, S., & Gaspar-Cunha, A. (2017). 
        Portfolio implementation risk management using evolutionary multiobjective optimization. 
        Applied Sciences, 7(10), 1079.
        """
        X = pop.get("X")

        W = X[:, :self.n_stocks]
        Y = X[:, self.n_stocks:]

        for i in range(len(W)):
            cardinality = Y[i].sum()
            #select more stocks to portfolio randomly to reach the minimum limit
            if cardinality < self.c_min:
                indicesOfZeros = [j for j in range(len(Y[i])) if Y[j] == 0]
                howManyMissing = self.c_min - cardinality
                clampI = np.random.choice(indicesOfZeros, howManyMissing, replace = False)
                Y[i][clampI] = 1
                W[i][clampI] = self.w_min
                cardinality = Y[i].sum()
            #select less stocks to portfolio to decrease to the maximum limit
            if cardinality > self.c_max:
                ones = [(j,W[i][j]) for j in range(len(Y[i])) if Y[j] == 1]
                howManyTooMany = cardinality - self.c_max
                onesSortedByWeight = sorted(ones, key=lambda x: x[1])
                clampI = map(lambda x:x[0], onesSortedByWeight[:howManyTooMany])
                Y[i][clampI] = 0
                W[i][clampI] = 0


        # pop.set("X", Xnorm.T)
        

        return pop

def main():
    r = OneSumRepair(0.1, 0.9, 4)
    W = np.array([
        [0.2, 0.4, 0.4, 0.1],
        [0.2, 0.2, 0.3, 0.3],
        [0.6, 0.7, 0.5, 0.9],
        [0.6, 0.7, 0.5, 0.9],
    ])
    Y = np.array([
        [1,1,0,1],
        [0,1,1,0],
        [1,1,1,1],
        [0,0,0,0],
    ], dtype=int)
    X = np.hstack((W,Y))

    P = r.do(None, Population.create(X))
    Res = P.get("X")
    print(Res)
    WW = Res[:,:4] * Res[:,4:]
    print(WW)
    print(WW.sum(axis=1))

# main()