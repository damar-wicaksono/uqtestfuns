import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    return np.sum(xx, axis=1)


def evaluate_with_parameters(
    xx: np.ndarray,
    coefficients: np.ndarray,
) -> np.ndarray:
    return np.sum(xx * coefficients, axis=1)


def get_coefficients(a, c) -> np.ndarray:
    return a * np.ones(3) + c
