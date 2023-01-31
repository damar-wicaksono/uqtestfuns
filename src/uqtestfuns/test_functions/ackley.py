"""
Module with an implementation of the M-dimensional Ackley function.

The Ackley function [1] is an M-dimensional non-convex scalar-valued function
typically used for testing optimization algorithms.
Originally the function is presented as a two-dimensional function.

References
----------

1. D. H. Ackley, "A connectionist machine for genetic hillclimbing."
   Boston, MA:  Kluwer Academic Publishers, 1987.
"""
import numpy as np

from ..core import UnivariateInput

DEFAULT_NAME = "Ackley"

TAGS = ["metamodeling", "optimization"]


def _ackley_input(spatial_dimension: int):
    """
    # TODO: complete the description here
    :param spatial_dimension:
    :return:
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivariateInput(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[-32.768, 32.768],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "ackley": {
        "name": "Ackley",
        "description": (
            "Probabilistic input model for the Ackley function "
            "from Ackley (1987)."
        ),
        "marginals": _ackley_input,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "ackley"

AVAILABLE_PARAMETERS = {"ackley": (20, 0.2, 2 * np.pi)}

DEFAULT_PARAMETERS_SELECTION = "ackley"

DEFAULT_DIMENSION = 2  # The dimension is variable so a default is given


def evaluate(xx: np.ndarray, params: tuple) -> np.ndarray:
    """Evaluate the Ackley function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    params : tuple
        A tuple of length 3 for the parameters of the Ackley function.

    Returns
    -------
    np.ndarray
        The output of the Ackley function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    m = xx.shape[1]
    a, b, c = params

    # Compute the Ackley function
    term_1 = -1 * a * np.exp(-1 * b * np.sqrt(np.sum(xx**2, axis=1) / m))
    term_2 = -1 * np.exp(np.sum(np.cos(c * xx), axis=1) / m)

    yy = term_1 + term_2 + a + np.exp(1)

    return yy
