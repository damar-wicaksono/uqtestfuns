"""
Module with an implementation of the Modified Sobol-G test function.

The modified Sobol'-G function, often written as Sobol'-G* function,
is a scalar-valued function in M dimensions.
It was first introduced in [1] to serve as a test function for sensitivity
analysis methods.
This function, which introduces shift and curvature parameters,
is a modification of the original Sobol'-G test function [2].

The function has found application in the study of sensitivity analysis, e.g.,
[3].

There are several sets of parameters used in the literature.

References
----------

1. A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto,
   and S. Tarantola, “Variance based sensitivity analysis of model output.
   Design and estimator for the total sensitivity index,”
   Computer Physics Communications, vol. 181, no. 2, pp. 259–270, 2010.
   DOI: 10.1016/j.cpc.2009.09.018
2. A. Saltelli and I. M. Sobol’, “About the use of rank transformation in
   sensitivity analysis of model output,” Reliability Engineering
   & System Safety, vol. 50, no. 3, pp. 225–239, 1995.
   DOI: 10.1016/0951-8320(95)00099-2.
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["SobolGStar"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Saltelli2010": {
        "function_id": "SobolGStar",
        "description": (
            "Probabilistic input model for the Sobol'-G* function "
            "from Saltelli et al. (2010)"
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


def _get_aa_saltelli_2010_a(input_dimension: int) -> np.ndarray:
    """Construct a coefficients array for the Sobol'-G* function from [1].

    Notes
    -----
    - This value is used in test case 1, 3, and 5 (see Table 5 in [1]).
    - In [1], an input dimension of 10 was used. If the input dimension is less
      than 10, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    - With the selected parameters, the function is of low effective dimension.
    """
    aa = 9 * np.ones(input_dimension)
    aa[:2] = 0

    return aa


def _get_aa_saltelli_2010_b(input_dimension: int) -> np.ndarray:
    """Construct a coefficients array for the Sobol'-G* function from [1].

    Notes
    -----
    - This value is used in test case 2, 5, and 6 (see Table 5 in [1]).
    - In [1], an input dimension of 10 was used. If the input dimension is less
      than 10, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    """
    aa = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1, 2, 3, 4])

    if input_dimension > 10:
        aa_ext = np.arange(5, input_dimension - 5)
        aa = np.append(aa, aa_ext)

    return aa[:input_dimension]


def _get_alpha_saltelli_2010_a(input_dimension: int) -> np.ndarray:
    """Construct an alpha array for the Sobol'-G* function from [1].

    Notes
    -----
    - This value is used in test case 1 and 2 (see Table 5 in [1]).
    - In [1], an input dimension of 10 was used. If the input dimension is less
      than 10, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    """
    alpha = np.ones(input_dimension)

    return alpha


def _get_alpha_saltelli_2010_b(input_dimension: int) -> np.ndarray:
    """Construct an alpha array for the Sobol'-G* function from [1].

    Notes
    -----
    - This value is used in test case 3 and 4 (see Table 5 in [1]).
    - In [1], an input dimension of 10 was used. If the input dimension is less
      than 10, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    """
    alpha = 0.5 * np.ones(input_dimension)

    return alpha


def _get_alpha_saltelli_2010_c(input_dimension: int) -> np.ndarray:
    """Construct an alpha array for the Sobol'-G* function from [1].

    Notes
    -----
    - This value is used in test case 5 and 6 (see Table 5 in [1]).
    - In [1], an input dimension of 10 was used. If the input dimension is less
      than 10, the parameters array is truncated; if the input dimension exceed
      10, the parameters are is extrapolated.
    """
    alpha = 2 * np.ones(input_dimension)

    return alpha


def _get_delta_saltelli_2010(input_dimension: int) -> np.ndarray:
    """Construct a delta array for the Sobol'-G* function from [1].

    The parameter delta (shift parameter) is randomly generated
    from a uniform distribution in [0, 1].
    """
    rng = np.random.default_rng()
    delta = rng.random(input_dimension)

    return delta


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Saltelli2010-1": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al."
            "(2010), test case 1; low-effective dimension, easier than "
            "test case 2"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_a,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_a,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
    "Saltelli2010-2": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al. "
            "(2010), test case 2; high-effective dimension, more difficult "
            "than test case 1"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_b,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_a,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
    "Saltelli2010-3": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al. "
            "(2010), test case 3; concave version of test case 1"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_a,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_b,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
    "Saltelli2010-4": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al. "
            "(2010), test case 4; concave version of test case 2"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_b,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_b,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
    "Saltelli2010-5": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al. "
            "(2010), test case 5; convex version of test case 1"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_a,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_c,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
    "Saltelli2010-6": {
        "function_id": "SobolGStar",
        "description": (
            "Parameter set for the Sobol-G* function from Saltelli et al. "
            "(2010), test case 6; convex version of test case 2"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_aa_saltelli_2010_b,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
            {
                "keyword": "delta",
                "value": _get_delta_saltelli_2010,
                "type": np.ndarray,
                "description": "Shift parameter",
            },
            {
                "keyword": "alpha",
                "value": _get_alpha_saltelli_2010_c,
                "type": np.ndarray,
                "description": "Curvature parameter",
            },
        ],
    },
}

DEFAULT_PARAMETERS_SELECTION = "Saltelli2010-1"


def evaluate(
    xx: np.ndarray,
    aa: np.ndarray,
    delta: np.ndarray,
    alpha: np.ndarray,
) -> np.ndarray:
    """Evaluate the modified Sobol-G function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of parameters (i.e., coefficients) of the modified Sobol'-G
        function; the length of the vector is the same as the number
        of input dimensions.
    delta: np.ndarray
        The vector of shift parameters of length M.
    alpha: np.ndarray
        The vector of curvature parameters of length M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    term = np.abs(2 * (xx + delta - np.floor(xx + delta)) - 1) ** alpha
    g_star = ((1 + alpha) * term + aa) / (1 + aa)

    yy = np.prod(g_star, axis=1)

    return yy


class SobolGStar(UQTestFunVarDimABC):
    """An implementation of the M-dimensional Sobol'-G* test function."""

    _tags = ["sensitivity"]
    _description = "Sobol'-G* function from Saltelli et al. (2010)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = DEFAULT_PARAMETERS_SELECTION

    evaluate = staticmethod(evaluate)  # type: ignore
