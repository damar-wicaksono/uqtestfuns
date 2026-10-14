import numpy as np


def evaluate(xx: np.ndarray):

    return np.ones((len(xx), 3, 10, 10)) + xx
