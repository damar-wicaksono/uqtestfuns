import numpy as np


def sum_eval(xx: np.ndarray) -> np.ndarray:
    return np.sum(xx, axis=1)


def prod_eval(xx: np.ndarray) -> np.ndarray:
    return np.prod(xx, axis=1)


def max_eval(xx: np.ndarray) -> np.ndarray:
    return np.max(xx, axis=1)
