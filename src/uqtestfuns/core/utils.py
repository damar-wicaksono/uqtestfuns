"""
Utility module for all the UQ test functions.
"""
from .prob_input import MultivariateInput


def create_canonical_uniform_input(
    spatial_dimension: int, min_value: float, max_value: float
) -> MultivariateInput:
    """Create a MultivariateInput in a canonical domain of [-1, 1]"""
    input_dicts = []
    for i in range(spatial_dimension):
        input_dicts.append(
            {
                "name": f"X{i+1}",
                "distribution": "uniform",
                "parameters": [min_value, max_value],
            }
        )

    return MultivariateInput(input_dicts)
