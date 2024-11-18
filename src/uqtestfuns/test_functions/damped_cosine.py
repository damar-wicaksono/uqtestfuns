"""
Module with an implementation the one-dimensional damped cosine function.


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

__all__ = ["DampedCosine"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Santner2018": {
        "function_id": "DampedCosine",
        "description": (
            "Input model for the one-dimensional damped cosine "
            "from Santner et al. (2018)"
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
    }
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 1D damped cosine function on a set of input values.

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
    yy = np.exp(-1.4 * xx[:, 0]) * np.cos(3.5 * np.pi * xx[:, 0])

    return yy


class DampedCosine(UQTestFunFixDimABC):
    """An implementation of the 1D damped cosine from Santner et al. (2018)."""

    _tags = ["metamodeling"]
    _description = "One-dimensional damped cosine from Santner et al. (2018)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None
    _default_input_dimension = 1

    evaluate = staticmethod(evaluate)  # type: ignore
