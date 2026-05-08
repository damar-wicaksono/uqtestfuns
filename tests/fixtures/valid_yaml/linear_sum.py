import numpy as np


def compute(xx: np.ndarray) -> np.ndarray:
    return np.sum(xx, axis=1)


def create_uniform_marginals(input_dimension: int):
    return [
        {
            "name": f"X{i + 1}",
            "distribution": "uniform",
            "parameters": [0.0, 1.0],
            "description": None,
        }
        for i in range(input_dimension)
    ]


def create_scaled_marginals(input_dimension: int, scale: float):
    return [
        {
            "name": f"X{i + 1}",
            "distribution": "uniform",
            "parameters": [0.0, scale * (i + 1)],
            "description": None,
        }
        for i in range(input_dimension)
    ]
