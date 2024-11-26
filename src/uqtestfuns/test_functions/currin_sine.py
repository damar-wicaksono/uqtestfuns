"""
Module with an implementation of the Sine function from Currin et al. (1988).

The one-dimensional, scalar-valued function was featured in [1] as an example
for Gaussian process metamodeling.

References
----------

1. C. Currin, T. Mitchell, M. Morris, and D. Ylvisaker,
   “A Bayesian Approach to the Design and Analysis of Computer Experiments,”
   ORNL-6498, 814584, 1988.
   DOI: 10.2172/814584
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["CurrinSine"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Currin1988": {
        "function_id": "CurrinSine",
        "description": (
            "Input model for the Sine function from Currin et al. (1988)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the sine fcn from Currin et al (1988) on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.sin(2 * np.pi * (xx[:, 0] - 0.1))

    return yy


class CurrinSine(UQTestFunFixDimABC):
    """A concrete implementation of the sine fcn from Currin et al (1988)."""

    _tags = ["metamodeling"]
    _description = "Sine function from Currin et al. (1988)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
