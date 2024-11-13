"""
This module implements the Sobol'-Levitan test function.

The Sobol'-Levitan function is an M-dimensional, scalar-valued function
commonly used as a benchmark for sensitivity analysis.
The function was introduced in [1] (as a six- and 20-dimensional functions)
and revisited in, for example, [2] (as a 20-dimensional function)
and [3] (as a seven- and 15-dimensional functions).

The Sobol' sensitivity indices of the test function can be derived analytically
as functions of the parameter.

References
----------

1. I. M. Sobol’ and Yu. L. Levitan, “On the use of variance reducing
   multipliers in Monte Carlo computations of a global sensitivity index,”
   Computer Physics Communications, vol. 117, no. 1–2, pp. 52–61, 1999.
   DOI: 10.1016/S0010-4655(98)00156-8
2. H. Moon, A. M. Dean, and T. J. Santner, “Two-Stage Sensitivity-Based Group
   Screening in Computer Experiments,” Technometrics*, vol. 54, no. 4,
   pp. 376–387, 2012.
   DOI: 10.1080/00401706.2012.725994
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from uqtestfuns.core.custom_typing import FunParamSpecs, ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["SobolLevitan"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Sobol1999": {
        "function_id": "SobolLevitan",
        "description": (
            "Probabilistic input model for the Sobol'-Levitan function "
            "from Sobol' and Levitan (1999)"
        ),
        "marginals": [
            {
                "name": "X",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


def _get_bb_sobol_1999_1(input_dimension: int) -> np.ndarray:
    """Construct the coefficients from Sobol' and Levitan (1999) 6D case.

    Notes
    -----
    - In [1], an input dimension of 6 was used. If the input dimension is less
      than 6, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    """
    bb = np.array([1.5, 0.9, 0.9, 0.9, 0.9, 0.9])

    if input_dimension > 6:
        bb_ext = 0.9 * np.ones(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


def _get_bb_sobol_1999_2(input_dimension: int) -> np.ndarray:
    """Construct the coefficients from Sobol' and Levitan (1999) 20D case.

    Notes
    -----
    - In [1], an input dimension of 20 was used. If the input dimension is less
      than 20, the parameters array is truncated; if the input dimension exceed
      20, the parameters are is extrapolated.
    """
    bb_1 = 0.6 * np.ones(10)
    bb_2 = 0.4 * np.ones(10)
    bb = np.append(bb_1, bb_2)

    if input_dimension > 20:
        bb_ext = 0.4 * np.ones(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


def _get_bb_moon_2012_1(input_dimension: int) -> np.ndarray:
    """Construct the coefficients from Moon et al. (2012) base case.

    Notes
    -----
    - In [1], an input dimension of 20 was used. If the input dimension is less
      than 20, the parameters array is truncated; if the input dimension exceed
      20, the parameters are is extrapolated.
    """
    bb = np.array(
        [
            2.0000,
            1.9500,
            1.9000,
            1.8500,
            1.8000,
            1.7500,
            1.7000,
            1.6500,
            0.4228,
            0.3077,
            0.2169,
            0.1471,
            0.0951,
            0.0577,
            0.0323,
            0.0161,
            0.0068,
            0.0021,
            0.0004,
            0.0000,
        ]
    )

    if input_dimension > 20:
        bb_ext = np.zeros(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Sobol1999-1": {
        "function_id": "SobolLevitan",
        "description": (
            "Parameter set for the M-dimensional function from "
            "Sobol' and Levitan (1999), 6D case"
        ),
        "declared_parameters": [
            {
                "keyword": "bb",
                "value": _get_bb_sobol_1999_1,
                "type": np.ndarray,
                "description": "Coefficients 'b'",
            },
            {
                "keyword": "c0",
                "value": 0.0,
                "type": float,
                "description": "Constant term",
            },
        ],
    },
    "Sobol1999-2": {
        "function_id": "SobolLevitan",
        "description": (
            "Parameter set for the M-dimensional function from "
            "Sobol' and Levitan (1999), 20D case"
        ),
        "declared_parameters": [
            {
                "keyword": "bb",
                "value": _get_bb_sobol_1999_2,
                "type": np.ndarray,
                "description": "Coefficients 'b'",
            },
            {
                "keyword": "c0",
                "value": 0.0,
                "type": float,
                "description": "Constant term",
            },
        ],
    },
    "Moon2012-1": {
        "function_id": "SobolLevitan",
        "description": (
            "Parameter set for the M-dimensional function from "
            "Moon et al. (2012), base case"
        ),
        "declared_parameters": [
            {
                "keyword": "bb",
                "value": _get_bb_moon_2012_1,
                "type": np.ndarray,
                "description": "Coefficients 'b'",
            },
            {
                "keyword": "c0",
                "value": 0.0,
                "type": float,
                "description": "Constant term",
            },
        ],
    },
}


DEFAULT_PARAMETERS_SELECTION = "Sobol1999-1"


def evaluate(xx: np.ndarray, bb: np.ndarray, c0: float) -> np.ndarray:
    """Evaluate the Sobol'-Levitan test function

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    bb : np.ndarray
        The coefficients of the function which control the importance of each
        input variable.
    c0 : float
        The constant term of the function.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    input_dim = xx.shape[1]
    ii = 1.0
    for i in range(input_dim):
        b = bb[i]
        # Safeguard against zero-value coefficient
        if b == 0:
            ii *= 1.0  # the limit as b approaches 0
        else:
            ii *= (np.exp(b) - 1) / b

    yy = np.exp(np.sum(bb * xx, axis=1)) - ii + c0

    return yy


class SobolLevitan(UQTestFunVarDimABC):
    """An implementation of the M-dimensional Sobol'-Levitan function."""

    _tags = ["sensitivity"]
    _description = "Test function from Sobol' and Levitan (1999)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = DEFAULT_PARAMETERS_SELECTION

    evaluate = staticmethod(evaluate)  # type: ignore
