"""
This module provides an implementation of the Rosenbrock function.

The Rosenbrock function, originally introduced in [1] as a two-dimensional
scalar-valued test function for global optimization, was later generalized
to M dimensions.
It has since become a widely used benchmark for global optimization methods
(e.g., [2], [3]).
In [4], the function was employed in a metamodeling exercise.

The function features a curved, non-convex valley.
While it is relatively easy to reach the valley, the convergence to the global
minimum is difficult.

References
----------
1. H. H. Rosenbrock, “An Automatic Method for Finding the Greatest or Least
   Value of a Function,” The Computer Journal, vol. 3, no. 3, pp. 175–184,
   1960.
   DOI: 10.1093/comjnl/3.3.175
2. L. C. W. Dixon and G. P. Szegö. Towards global optimization 2,
   chapter The global optimization problem: an introduction, pages 1–15.
   North-Holland, Amsterdam, 1978.
3. V. Picheny, T. Wagner, and D. Ginsbourger, “A benchmark of kriging-based
   infill criteria for noisy optimization,” Structural and Multidisciplinary
   Optimization, vol. 48, no. 3, pp. 607–626, 2013.
   DOI: 10.1007/s00158-013-0919-4
4. M. H. Y. Tan, “Stochastic Polynomial Interpolation for Uncertainty
   Quantification With Computer Experiments,” Technometrics, vol. 57, no. 4,
   pp. 457–467, 2015.
   DOI: 10.1080/00401706.2014.950431
"""

import numpy as np

from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC
from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs

__all__ = ["Rosenbrock"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Picheny2013": {
        "function_id": "Rosenbrock",
        "description": (
            "Search domain for the Rosenbrock function from Picheny et al. "
            "(2013)"
        ),
        "marginals": [
            {
                "name": "x",
                "distribution": "uniform",
                "parameters": [-5.0, 10.0],
                "description": None,
            },
        ],
        "copulas": None,
    }
}


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Rosenbrock1960": {
        "function_id": "Rosenbrock",
        "description": (
            "Parameter set for the Rosenbrock function from Rosenbrock (1960)"
        ),
        "declared_parameters": [
            {
                "keyword": "a",
                "value": 1.0,
                "type": float,
                "description": "Global optimum location and value",
            },
            {
                "keyword": "b",
                "value": 100.0,
                "type": float,
                "description": (
                    "Steepness, curvature, and width of the valley"
                ),
            },
            {
                "keyword": "c",
                "value": 0.0,
                "type": float,
                "description": "Shift parameter",
            },
            {
                "keyword": "d",
                "value": 1.0,
                "type": float,
                "description": "Scale parameter",
            },
        ],
    },
}


def evaluate(
    xx: np.ndarray, a: float, b: float, c: float, d: float
) -> np.ndarray:
    """Evaluate the Rosenbrock function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    a : float
        The parameter controlling the magnitude of the quadratic penalty term
        between a given input and the parameter; the global optimum location
        and value are controlled by this parameter.
    b : float
        The parameter controlling the magnitude of the quadratic penalty term
        between two adjacent input variables; the steepness, curvature, and
        width of the valley are controlled by this parameter.
    c : float
        The shift parameter.
    d : float
        The scale parameter.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.

    Notes
    -----
    - The function returns a constant zero for M < 2.
    """
    if xx.shape[1] == 1:
        return np.zeros(xx.shape[0])

    yy = (xx[:, :-1] - a) ** 2 + b * (xx[:, 1:] - xx[:, :-1] ** 2) ** 2
    yy = np.sum(yy, axis=1)
    # Shift and rescale
    yy = (yy - c) / d

    return yy


class Rosenbrock(UQTestFunVarDimABC):
    """A concrete implementation of the Rosenbrock test function."""

    _tags = ["optimization", "metamodeling"]
    _description = (
        "Optimization test function from Rosenbrock (1960), "
        "also known as the banana function"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS

    evaluate = staticmethod(evaluate)  # type: ignore
