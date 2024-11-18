"""
Module with implementations of the two functions from Lim et al. (2002).

The test functions are two-dimensional scalar-valued functions used in [1]
to illustrate the connection between Gaussian process metamodels and
polynomials.

References
----------

1. Y. B. Lim, J. Sacks, W. J. Studden, and W. J. Welch, “Design and analysis of
   computer experiments when the output is highly correlated over the input
   space,” Canadian Journal of Statistics, vol. 30, no. 1, pp. 109–126, 2002,
   DOI: 10.2307/3315868
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs, MarginalSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["LimPoly", "LimNonPoly"]


MARGINALS_LIM2002: MarginalSpecs = [
    {
        "name": "x1",
        "distribution": "uniform",
        "parameters": [0.0, 1.0],
        "description": None,
    },
    {
        "name": "x2",
        "distribution": "uniform",
        "parameters": [0.0, 1.0],
        "description": None,
    },
]


def evaluate_poly(xx: np.ndarray) -> np.ndarray:
    """Evaluate the polynomial test function from Lim et al (2002).

    The function is a polynomial with maximum total degree of 5.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    trm_1 = 5.0 / 2.0 * xx[:, 0]
    trm_2 = 35.0 / 2.0 * xx[:, 1]
    trm_3 = 5.0 / 2.0 * xx[:, 0] * xx[:, 1]
    trm_4 = 19 * xx[:, 1] ** 2
    trm_5 = 15.0 / 2.0 * xx[:, 0] ** 3
    trm_6 = 5.0 / 2.0 * xx[:, 0] * xx[:, 1] ** 2
    trm_7 = 11.0 / 2.0 * xx[:, 1] ** 4
    trm_8 = xx[:, 0] ** 3 * xx[:, 1] ** 2

    yy = 9 + trm_1 - trm_2 + trm_3 + trm_4 - trm_5 - trm_6 - trm_7 + trm_8

    return yy


class LimPoly(UQTestFunFixDimABC):
    """An implementation of the 2D polynomial from Lim et al. (2002)."""

    _tags = ["metamodeling"]
    _description = "Two-dimensional polynomial function from Lim et al. (2002)"
    _available_inputs: ProbInputSpecs = {
        "Lim2002": {
            "function_id": "LimPoly",
            "description": (
                "Input specification for the polynomial function "
                "from Lim et al. (2002)"
            ),
            "marginals": MARGINALS_LIM2002,
            "copulas": None,
        }
    }
    _available_parameters = None

    evaluate = staticmethod(evaluate_poly)  # type: ignore


def evaluate_non_poly(xx: np.ndarray) -> np.ndarray:
    """Evaluate the non-polynomial test function from Lim et al (2002).

    The function is a polynomial with maximum total degree of 5.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    trm_1 = 30 + 5 * xx[:, 0] * np.sin(5 * xx[:, 0])
    trm_2 = 4 + np.exp(-5 * xx[:, 1])

    yy = (trm_1 * trm_2 - 100) / 6.0

    return yy


class LimNonPoly(UQTestFunFixDimABC):
    """An implementation of the 2D non-polynomial from Lim et al. (2002)."""

    _tags = ["metamodeling"]
    _description = (
        "Two-dimensional non-polynomial function from Lim et al. (2002)"
    )
    _available_inputs: ProbInputSpecs = {
        "Lim2002": {
            "function_id": "LimNonPoly",
            "description": (
                "Input specification for the non-polynomial function "
                "from Lim et al. (2002)"
            ),
            "marginals": MARGINALS_LIM2002,
            "copulas": None,
        }
    }
    _available_parameters = None

    evaluate = staticmethod(evaluate_non_poly)  # type: ignore
