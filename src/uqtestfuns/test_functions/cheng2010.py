"""
Module with an implementation of the 2D function from Cheng and Sandu (2010).

The two-dimensional function was used in [1] as an example for metamodeling
using polynomial chaos expansion.

References
----------
1. H. Cheng and A. Sandu, “Collocation least-squares polynomial chaos method,”
   in Proceedings of the 2010 Spring Simulation Multiconference, Orlando,
   Florida: Society for Computer Simulation International, 2010, pp. 1–6.
   DOI: 10.1145/1878537.1878621.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Cheng2D"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Cheng2010": {
        "function_id": "Cheng2D",
        "description": (
            "Probabilistic input model for the 2D test function "
            "from Cheng and Sandu (2010)"
        ),
        "marginals": [
            {
                "name": "X1",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 2D test function from Cheng and Sandu (2010).

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.cos(np.sum(xx, axis=1)) * np.exp(np.prod(xx, axis=1))

    return yy


class Cheng2D(UQTestFunFixDimABC):
    """Concrete implementation of the function from Cheng and Sandu (2010)."""

    _tags = ["metamodeling"]
    _description = "Two-dimensional test function from Cheng and Sandu (2010)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
