import numpy as np


def evaluate(
    xx: np.ndarray,
    scale: float,
    coefficients: np.ndarray,
    factors: np.ndarray,
    bounds: dict,
) -> np.ndarray:
    raw = scale * np.sum(factors * coefficients * xx, axis=1)
    return np.clip(raw, bounds["lower"], bounds["upper"])


def get_coefficients(input_dimension: int) -> np.ndarray:
    return np.arange(1, input_dimension + 1, dtype=float)


def get_factors() -> np.ndarray:
    return np.array([1.0, 2.0, 3.0])


def create_fixed_marginals():
    marginals = []
    for i in range(3):
        marginals.append(
            {
                "name": f"X{i + 1}",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            }
        )

    return marginals
