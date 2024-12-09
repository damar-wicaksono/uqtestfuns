"""
Module with an implementation of the Friedman test functions.

The Friedman function is a function introduced in [2] as a six-dimensional
(including one dummy variable) test function for testing a spline approximation
method. It was later modified to be a ten-dimensional (including five dummy
variables) function in [2].
In [3], the function was employed as a test function in the context of
sensitivity analysis.

References
----------

1. J. H. Friedman, E. Grosse, and W. Stuetzle, "Multidimensional additive
   spline approximation," SIAM Journal on Scientific and Statistical Computing,
   vol. 4, no. 2, pp. 291-301, 1983.
2. J. H. Friedman, "Multivariate adaptive regression splines," The Annals of
   Statistics, vol. 19, no. 1, pp. 1-67, 1991.
   DOI: 10.1214/aos/1176347963
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental
   Modelling & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Friedman6D", "Friedman10D"]


AVAILABLE_INPUTS_6D: ProbInputSpecs = {
    "Friedman1983": {
        "function_id": "Friedman6D",
        "description": (
            "Input specification for the 6D test function "
            "from Friedman et al. (1983)"
        ),
        "marginals": [
            {
                "name": f"x_{i + 1}",
                "distribution": "uniform",
                "parameters": [0, 1],
                "description": None,
            }
            for i in range(6)
        ],
        "copulas": None,
    },
}


AVAILABLE_INPUTS_10D: ProbInputSpecs = {
    "Friedman1983": {
        "function_id": "Friedman10D",
        "description": (
            "Input specification for the 6D test function "
            "from Friedman (1991)"
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


def evaluate_friedman(xx: np.ndarray) -> np.ndarray:
    """Evaluate the six-dimensional Friedman test function.

    Parameters
    ----------
    xx : np.ndarray
        6-Dimensional input values given by an N-by-M array
        where N is the number of input values and M >= 5 is the number of
        input dimensions.

    Returns
    -------
    np.ndarray
        The output of the six-dimensional Friedman function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.

    Notes
    -----
    - Only the first five input variables are active; the rest is inactive.
    """
    yy_1 = 10 * np.sin(np.pi * xx[:, 0] * xx[:, 1])
    yy_2 = 20 * (xx[:, 2] - 0.5) ** 2
    yy_3 = 10 * xx[:, 3]
    yy_4 = 5 * xx[:, 4]

    return yy_1 + yy_2 + yy_3 + yy_4


class Friedman6D(UQTestFunFixDimABC):
    """A concrete implementation of the 6D Friedman et al. (1983) function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Six-dimensional function from Friedman et al. (1983)"
    _available_inputs = AVAILABLE_INPUTS_6D
    _available_parameters = None

    evaluate = staticmethod(evaluate_friedman)  # type: ignore


class Friedman10D(UQTestFunFixDimABC):
    """A concrete implementation of the 10D Friedman (1991) function."""

    _tags = ["metamodeling"]
    _description = "Ten-dimensional function from Friedman (1991)"
    _available_inputs = AVAILABLE_INPUTS_10D
    _available_parameters = None

    evaluate = staticmethod(evaluate_friedman)  # type: ignore
