import itertools
import math
import numpy as np
from pymoo.core.repair import Repair
from pymoo.core.population import Population

class OneSumRepair(Repair):
    def _do(self, problem, pop, **kwargs):
        """
        Transforms weight vectors into feasible ones
        so that for each row the sum is 1
        Kaucic, M., Moradi, M., & Mirzazadeh, M. (2019). 
        Portfolio optimization by improved NSGA-II and SPEA 2 based on different risk measures. 
        Financial Innovation, 5(1), 1-28.
        """
        X = pop.get("X")
        X01 = X.clip(0, 1)
        Xsum = X01.sum(axis=1)
        Xnorm = X01.T / Xsum
        pop.set("X", Xnorm.T)
        return pop

# print(repair(np.array([[0,1,2], [1/3, 1/3, 1/3], [0.25, 0.25, 1]])))
def createWeightVectors(n_vectors, n_weights):
    """
    Creates weight vectors
    """
    repair = OneSumRepair()
    X = np.random.random((n_vectors,n_weights))
    P = Population.create(X)
    W = repair.do(None, P)
    return W
