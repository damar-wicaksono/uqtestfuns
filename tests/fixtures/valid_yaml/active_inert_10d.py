import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    return np.sum(xx[:, :3], axis=1)
