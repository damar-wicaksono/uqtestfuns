import numpy as np


def evaluate(xx: np.ndarray, p: float) -> np.ndarray:
    return p - xx[:, 0] ** 2 - xx[:, 1] ** 2
