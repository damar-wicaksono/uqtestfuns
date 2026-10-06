import numpy as np


def evaluate(xx: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.prod(1.0 + weights * xx, axis=1)


def get_equal_weights(input_dimension: int) -> np.ndarray:
    return np.ones(input_dimension)


def get_decaying_weights(input_dimension: int, rate: float) -> np.ndarray:
    return 1.0 / np.arange(1, input_dimension + 1, dtype=float) ** rate
