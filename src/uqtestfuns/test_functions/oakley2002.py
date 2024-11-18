"""
Module with implementations of test functions from Oakley and O'Hagan (2002).

The 1D test function from Oakley and O'Hagan (2002) (or `Oakley1D` function
for short) is a one-dimensional scalar-valued function.
It was used in [1] as a test function for illustrating metamodeling
and uncertainty propagation approaches.

References
----------

1. Jeremy Oakley and Anthony O'Hagan, "Bayesian inference for the uncertainty
   distribution of computer model outputs," Biometrika , Vol. 89, No. 4,
   p. 769-784, 2002.
   DOI: 10.1093/biomet/89.4.769
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Oakley1D"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Oakley2002": {
        "function_id": "Oakley1D",
        "description": (
            "Probabilistic input model for the one-dimensional function "
            "from Oakley and O'Hagan (2002)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "normal",
                "parameters": [0.0, 4.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 1D Oakley-O'Hagan function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 1D Oakley-O'Hagan function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 5 + xx[:, 0] + np.cos(xx[:, 0])

    return yy


class Oakley1D(UQTestFunFixDimABC):
    """An implementation of the 1D function from Oakley & O'Hagan (2002)."""

    _tags = ["metamodeling"]
    _description = "One-dimensional function from Oakley and O'Hagan (2002)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
