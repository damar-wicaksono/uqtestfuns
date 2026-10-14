import numpy as np


def evaluate(xx: np.ndarray, n_t: int):

    yy = np.linspace(0, 1, n_t)

    return np.ones((len(xx), len(yy))) + xx


def output_shape(n_t: int, **kwargs):

    return (n_t,)
