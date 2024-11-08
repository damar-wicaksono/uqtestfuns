"""
Module with an implementation of the Quadratic RS reliability problem.

The two-dimensional function is a variant of the classic RS reliability problem
with one quadratic term [1].

References
----------
1. Paul Hendrik Waarts, “Structural reliability using finite element
   analysis - an appraisal of DARS: Directional adaptive response surface
   sampling," Civil Engineering and Geosciences, TU Delft, Delft,
   The Netherlands, 2000.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["RSQuadratic"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Waarts2000": {
        "function_id": "RSQuadratic",
        "description": "Input model for the quadratic RS from Waarts (2000)",
        "marginals": [
            {
                "name": "X1",
                "distribution": "normal",
                "parameters": [11.0, 1.0],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "normal",
                "parameters": [1.5, 0.5],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the quadratic RS function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The performance function of the problem.
        If negative, the system is in failed state.
        The output is a one-dimensional array of length N.
    """

    # Compute the performance function
    yy = xx[:, 0] - xx[:, 1] ** 2

    return yy


class RSQuadratic(UQTestFunFixDimABC):
    """Concrete implementation of the quadratic RS reliability problem."""

    _tags = ["reliability"]
    _description = "RS problem w/ one quadratic term from Waarts (2000)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None
    _default_input_dimension = 2

    evaluate = staticmethod(evaluate)  # type: ignore
