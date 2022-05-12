import itertools
import math
import numpy as np
from pymoo.core.repair import Repair

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

