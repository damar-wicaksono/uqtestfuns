"""
Module with an implementation of the functions from Linkletter et al. (2006)

The paper by Linkletter et al. (2006) [1] contains four analytical test
functions used for sensitivity analysis in the context of variable selection
in Gaussian process metamodeling.
All functions are defined in ten dimensions but some of them are inactive.

Available functions are:

- Linear function with four active input variables (out of 10).

References
----------

1. C. Linkletter, D. Bingham, N. Hengartner, D. Higdon, and K. Q. Ye,
   “Variable Selection for Gaussian Process Models in Computer Experiments,”
   Technometrics, vol. 48, no. 4, pp. 478–490, 2006.
   DOI: 10.1198/004017006000000228.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["LinkletterLinear"]


def evaluate_linear(xx: np.ndarray) -> np.ndarray:
    """Evaluate the linear  function from Linkletter et al. (2006).

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-10 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 0.2 * np.sum(xx[:, :4], axis=1)

    return yy


class LinkletterLinear(UQTestFunFixDimABC):
    """A concrete implementation of the linear function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Linear function from Linkletter et al. (2006)"
    _available_inputs: ProbInputSpecs = {
        "Linkletter2006": {
            "function_id": "LinkletterLinear",
            "description": (
                "Input specification for the linear test function Eq. (5)"
                "from Linkletter et al. (2006)"
            ),
            "marginals": [
                {
                    "name": f"x_{i + 1}",
                    "distribution": "uniform",
                    "parameters": [0, 1],
                    "description": None,
                }
                for i in range(10)
            ],
            "copulas": None,
        },
    }
    _available_parameters = None

    evaluate = staticmethod(evaluate_linear)  # type: ignore
