"""
Utility module for all the UQ test functions.
"""
from .prob_input.univariate_input import UnivariateInput
from .prob_input.multivariate_input import MultivariateInput


def create_canonical_uniform_input(
    spatial_dimension: int, min_value: float, max_value: float
) -> MultivariateInput:
    """Create a MultivariateInput in a canonical domain of [-1, 1]"""
    marginals = []
    for i in range(spatial_dimension):

        marginals.append(
            UnivariateInput(
                name=f"X{i+1}",
                distribution="uniform",
                parameters=[min_value, max_value],
            )
        )

    return MultivariateInput(marginals)
