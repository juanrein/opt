import itertools
import math
import numpy as np
from pymoo.core.repair import Repair
from pymoo.core.population import Population
from sklearn.utils import indices_to_mask




class OneSumRepair(Repair):
    def __init__(self, n_stocks) -> None:
        super().__init__()
        self.n_stocks = n_stocks

    def _do(self, problem, pop, **kwargs):
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
        
        W01 = W.clip(0, 1)
        Wsum = W01.sum(axis=1)
        Wnorm = W01.T / Wsum
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
    def __init__(self, w_min, w_max, c_min, c_max) -> None:
        super().__init__()
        self.w_min = w_min
        self.w_max = w_max
        self.c_min = c_min
        self.c_max = c_max

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

        # pop.set("X", Xnorm.T)
        

        return pop

def main():
    r = BoundedRepair(0.1, 0.9, 2, 3)
    W = np.array([
        [0.2, 0.4, 0.4, 0], #feasible
        [0.2, 0.2, 0.3, 0.3], #too many
        [1.0, 0, 0, 0], #too few
        [0.05, 0.25, 0.7, 0], #loo low
        [0.3, 0.4, 0.5, 0.6], #not 1
    ])
    P = r.do(None, Population.create(W))
    print(P.get("X"))

# main()