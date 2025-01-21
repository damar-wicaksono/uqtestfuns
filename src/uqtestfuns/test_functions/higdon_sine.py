"""
Module with an implementation of the Sine function from Higdon (2002).

The one-dimensional, scalar-valued function was featured in [1] as an example
for a multi-resolution spatial modeling technique.

References
----------

1. D. Higdon, “Space and Space-Time Modeling using Process Convolutions,”
   in Quantitative Methods for Current Environmental Issues, C. W. Anderson,
   V. Barnett, P. C. Chatwin, and A. H. El-Shaarawi, Eds.,
   London: Springer London, 2002, pp. 37–56.
   DOI: 10.1007/978-1-4471-0657-9_2.

"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["HigdonSine"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Higdon2002": {
        "function_id": "HigdonSine",
        "description": (
            "Input model for the sine function from Higdon (2002)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "uniform",
                "parameters": [1.0, 10.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Higdon sine function on a set of input values.

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
    yy = np.sin(2 * np.pi * xx / 10) + 0.2 * np.sin(2 * np.pi * xx / 2.5)

    return yy


class HigdonSine(UQTestFunFixDimABC):
    """A concrete implementation of the Higdon sine function."""

    _tags = ["metamodeling"]
    _description = "Sine function from Higdon (2002)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
