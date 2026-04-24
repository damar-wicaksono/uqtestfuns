import numpy as np


def evaluate(
    xx: np.ndarray,
    scale: float,
    coefficients: np.ndarray,
    bounds: dict,
) -> np.ndarray:
    raw = scale * np.sum(coefficients * xx, axis=1)
    return np.clip(raw, bounds["lower"], bounds["upper"])


def get_coefficients(input_dimension: int) -> np.ndarray:
    return np.arange(1, input_dimension + 1, dtype=float)
