"""
Module with an implementation of the Sine function from Holsclaw et al. (2013).

The one-dimensional, scalar-valued function was featured in [1] as an example
for Gaussian process metamodeling.

References
----------

1. T. Holsclawy, B. Sansó, H. K H. Lee, K. Heitmann, S. Habib, D. Higdon, and
   U. Alam, “Gaussian Process Modeling of Derivative Curves,” Technometrics,
   vol. 55, no. 1, pp. 57–67, 2013.
   DOI: 10.1080/00401706.2012.723918.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["HolsclawSine"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Holsclaw2013": {
        "function_id": "HolsclawSine",
        "description": (
            "Input model for the sine function from Holsclaw et al. (2013)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "uniform",
                "parameters": [0.0, 10.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Holsclaw sine function on a set of input values.

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
    yy = xx * np.sin(xx) / 10

    return yy


class HolsclawSine(UQTestFunFixDimABC):
    """A concrete implementation of the Holsclaw sine function."""

    _tags = ["metamodeling"]
    _description = "Sine function from Holsclaw et al. (2013)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
