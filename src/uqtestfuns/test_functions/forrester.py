"""
Module with an implementation of the Forrester et al. (2008) test function.

The Forrester2008 test function is a one-dimensional scalar-valued function.
The function is multimodal, with a single global minimum, a single local
minimum, and a zero-gradient at the inflection point.

References
----------

1. William J. Welch, Robert J. Buck, Jerome Sacks, Henry P. Wynn,
   Toby J. Mitchell, and Max D. Morris, "Screening, predicting, and computer
   experiments," Technometrics, vol. 34, no. 1, pp. 15-25, 1992.
   DOI: 10.2307/1269548
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Forrester2008"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Forrester2008": {
        "function_id": "Forrester2008",
        "description": (
            "Input specification for the 1D test function "
            "from Forrester et al. (2008)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "uniform",
                "parameters": [0, 1],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """The evaluation function for the Forrester et al. (2008) function.

    Parameters
    ----------
    xx : np.ndarray
        One-dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 1D Forrester et al. (2008) function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (6 * xx[:, 0] - 2) ** 2 * np.sin(12 * xx[:, 0] - 4)

    return yy


class Forrester2008(UQTestFunFixDimABC):
    """An implementation of the 1D function of Forrester et al. (2008)."""

    _tags = ["optimization", "metamodeling"]
    _description = "One-dimensional function from Forrester et al. (2008)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
