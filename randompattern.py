import numpy as np


def random(n):
    r = np.random.random(n)
    ret = []
    for i in range(0, n):
        if r[i] < 0.03:
            ret.append(-100)
        elif r[i] > 0.97:
            ret.append(100)
        else:
            ret.append(0)
    return ret
