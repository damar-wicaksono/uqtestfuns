import numpy as np


def evaluate(xx: np.ndarray, a: float, b: float) -> np.ndarray:
    return a * np.sum(np.sin(b * xx), axis=1)
