"""
Module with an implementation of the Gayton Hat test function.

The Gayton Hat function is a two-dimensional limit-state function used
in [1] as a test function for reliability analysis algorithms.

References
----------

1. B. Echard, N. Gayton, M. Lemaire, and N. Relun, “A combined Importance
   Sampling and Kriging reliability method for small failure probabilities
   with time-demanding numerical models”, Reliability Engineering
   and System Safety, vol. 111, pp. 232-240, 2013.
   DOI: 10.1016/j.ress.2012.10.008
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["GaytonHat"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Echard2013": {
        "function_id": "GaytonHat",
        "description": (
            "Input model for the Gayton Hat function "
            "from Echard et al. (2013)"
        ),
        "marginals": [
            {
                "name": "U1",
                "distribution": "normal",
                "parameters": [0, 1],
                "description": None,
            },
            {
                "name": "U2",
                "distribution": "normal",
                "parameters": [0, 1],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Gayton Hat function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-Dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 0.5 * (xx[:, 0] - 2) ** 2 - 1.5 * (xx[:, 1] - 5) ** 3 - 3

    return yy


class GaytonHat(UQTestFunFixDimABC):
    """A concrete implementation of the Gayton Hat test function."""

    _tags = ["reliability"]
    _description = (
        "Two-Dimensional Gayton Hat function from Echard et al. (2013)"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None
    _default_input_dimension = 2

    evaluate = staticmethod(evaluate)  # type: ignore
