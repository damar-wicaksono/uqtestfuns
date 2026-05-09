"""
Module with an implementation of the 3D test function from Moon (2010).

The Moon3D function is a three-dimensional scalar-valued function used in
[1] to illustrate the analytical derivation of Sobol' sensitivity indices.

References
----------

1. H. Moon, "Design and Analysis of Computer Experiments for Screening Input
   Variables," Ph.D. dissertation, Ohio State University, Ohio, 2010.
   URL: http://rave.ohiolink.edu/etdc/view?acc_num=osu1275422248
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Moon3D"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Moon2010": {
        "function_id": "Moon3D",
        "description": (
            "Probabilistic input model for the 3D test function "
            "from Moon (2010)"
        ),
        "marginals": [
            {
                "name": "X1",
                "distribution": "uniform",
                "parameters": [0, 1],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "uniform",
                "parameters": [0, 1],
                "description": None,
            },
            {
                "name": "X3",
                "distribution": "uniform",
                "parameters": [0, 1],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """The evaluation function for the Moon (2010) 3D function.

    Parameters
    ----------
    xx : np.ndarray
        One-dimensional input values given by an N-by-3 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = xx[:, 0] + xx[:, 1] + 3 * xx[:, 0] * xx[:, 2]

    return yy


class Moon3D(UQTestFunFixDimABC):
    """An implementation of the 3D function of Moon (2010)."""

    _tags = ["sensitivity"]
    _description = "Three-dimensional function from Moon (2010)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
