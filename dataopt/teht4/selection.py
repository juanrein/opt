import math

def probability_wrong(A, stdA, B, stdB):
    """
    Computes the probability of choosing A wrongly
    when minimizing using hyperbolic tangent approximation
    with approximated function values A and B 
    and their standard deviations stdA and stdB
    """
    if math.isclose(stdA, 0):
        stdA += 1e-7
    if math.isclose(stdB, 0):
        stdB += 1e-7

    m = (A-B) / stdB
    s = stdA / stdB
    inside = m / (0.8 * math.sqrt(2.0 + 2.0 * s**2.0))
    return 0.5 * (1.0 + math.tanh(inside))


def compute_ranking(F, stds):
    """
    Computes ranking of objective function values
    where best (smallest value gets smallest ranking)
    """
    R = []
    for i in range(len(F)):
        Ri = -0.5
        for j in range(len(F)):
            Ri += probability_wrong(F[i], stds[i], F[j], stds[j])
        R.append(Ri)
    return R

def probability_of_selection(F, stds):
    """
    Compute probability for each function value that it
    should be selected based on objective function
    values F and their correspoding
    standard deviations stds
    """
    R = compute_ranking(F, stds)
    P = []
    n = len(R)
    for i in range(len(R)):
        p = (2 * ((n-1) - R[i])) / (n*(n-1))
        P.append(p)
    return P


