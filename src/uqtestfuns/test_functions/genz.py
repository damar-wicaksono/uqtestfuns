"""
Module with implementations of integral test functions from Genz (1984).

Genz [1] introduced six challenging parameterized $M$-dimensional functions
designed to test the performance of numerical integration routines:

- Corner peak function features a prominent peak in one corner
  of the multidimensional space.

The functions are further characterized by shift and scale parameters.
While the shift parameter has minimal impact on the integral's value,
the scale parameter significantly affects
the difficulty of the integration problem.

Some of the functions were featured as test functions in sensitivity
analysis literature, e.g., [2].

References
----------

1. A. Genz, “Testing Multidimensional Integration Routines,”
   in Proc. of International Conference on Tools, Methods and Languages
   for Scientific and Engineering Computation, USA: Elsevier North-Holland,
   Inc., 1984, pp. 81–94.
2. X. Zhang and M. D. Pandey, “An effective approximation for variance-based
   global sensitivity analysis,” Reliability Engineering & System Safety,
   vol. 121, pp. 164–174, 2014.
   DOI: 10.1016/j.ress.2013.07.010
"""

import numpy as np

from uqtestfuns.core.custom_typing import (
    FunParamSpecs, MarginalSpecs, ProbInputSpecs
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["GenzCornerPeak"]


MARGINALS_GENZ1984: MarginalSpecs = [
    {
        "name": "X",
        "distribution": "uniform",
        "parameters": [0.0, 1.0],
        "description": None,
    }
]

COMMON_TAGS = ["integration", "sensitivity"]


def _get_aa_genz_1984(input_dimension: int) -> np.ndarray:
    """Construct a scaling array for the Genz function from [1]."""
    aa = 5.0 * np.ones(input_dimension)

    return aa


def _get_aa_zhang_2014_1(input_dimension: int) -> np.ndarray:
    """Construct a scaling array for the Genz function from [2] (3D case).

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    - The test function was originally limited to three dimensions; here,
      the values beyond dimension 3 are extrapolated.
    """
    aa = 0.02 + 0.03 * np.arange(input_dimension)

    return aa


def _get_aa_zhang_2014_2(input_dimension: int) -> np.ndarray:
    """Construct a scaling array for the Genz function from [2] (10D case).

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    - The test function was originally limited to ten dimensions; here,
      the values beyond dimension 10 are extrapolated.
    """
    aa = 0.1 * np.arange(1, input_dimension + 1)

    return aa


def evaluate_corner_peak(xx: np.ndarray, aa: np.ndarray) -> np.ndarray:
    """Evaluate the corner peak function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of scale parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    dim = xx.shape[1]

    yy = (1 + (xx @ aa))**(-(dim + 1))

    return yy


class GenzCornerPeak(UQTestFunVarDimABC):
    """A concrete implementation of the corner peak from Genz (1984)."""

    _tags = COMMON_TAGS
    _description = "Corner peak integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Genz (1984)"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Scaling parameter",
                },
            ],
        },
        "Zhang2014-1": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Zhang and "
                "Pandey (2014); Section 4.4 (3D case)"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_zhang_2014_1,
                    "type": np.ndarray,
                    "description": "Scaling parameter",
                },
            ],
        },
        "Zhang2014-2": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Zhang and "
                "Pandey (2014); Section 4.4 (10D case)"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_zhang_2014_2,
                    "type": np.ndarray,
                    "description": "Scaling parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_corner_peak)  # type: ignore
