"""
Module with an implementation of the Bratley et al. (1992) test functions.

The Bratley et al. (1992) paper [1] contains four M-dimensional scalar-valued
functions for testing multi-dimensional numerical integrations using low
discrepancy sequences. The functions was used in [2] and [3] in the context
of global sensitivity analysis.

The four functions are:

- Bratley1992b: A product of trigonometric function;
  integration test function #2
- Bratley1992d: A sum of products integrand; integration test function #4

The Bratley1992d function may also be referred to as the "Bratley function"
or "Bratley et al. (1992) function" in the literature.

References
----------

1. Paul Bratley, Bennet L. Fox, and Harald Niederreiter, "Implementation and
   tests of low-discrepancy sequences," ACM Transactions on Modeling and
   Computer Simulation, vol. 2, no. 3, pp. 195-213, 1992.
   DOI:10.1145/146382.146385
2. S. Kucherenko, M. Rodriguez-Fernandez, C. Pantelides, and N. Shah,
   “Monte Carlo evaluation of derivative-based global sensitivity measures,”
   Reliability Engineering & System Safety, vol. 94, pp. 1137–1148, 2009.
   DOI:10.1016/j.ress.2008.05.006
3. A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto,
   and S. Tarantola, “Variance based sensitivity analysis of model output.
   Design and estimator for the total sensitivity index,” Computer Physics
   Communications, vol. 181, no. 2, pp. 259–270, 2010,
   DOI:10.1016/j.cpc.2009.09.018
"""

import numpy as np

from scipy.special import eval_chebyt

from .sobol_g import evaluate as evaluate_sobol_g

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["Bratley1992a", "Bratley1992b", "Bratley1992c", "Bratley1992d"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Bratley1992": {
        "function_id": "Bratley1992",
        "description": (
            "Integration domain of the functions from Bratley et al. (1992)"
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

# Common metadata used in each class definition of Bratley test functions
COMMON_METADATA = dict(
    _tags=["integration", "sensitivity"],
    _available_inputs=AVAILABLE_INPUTS,
    _available_parameters=None,
    _description="from Bratley et al. (1992)",
)


def evaluate_bratley1992a(xx: np.ndarray) -> np.ndarray:
    """Evaluate the test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    # The function is the Sobol'-G function with all the parameters set to 0.
    parameters = np.zeros(xx.shape[1])
    yy = evaluate_sobol_g(xx, parameters)

    return yy


class Bratley1992a(UQTestFunVarDimABC):
    """An implementation of the test function 1 from Bratley et al. (1992).

    The function (used as an integrand) is a product of an absolute function.

    Notes
    -----
    - The function is the Sobol'-G function with all the parameters set to 0.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = (
        f"Integration test function #1 {COMMON_METADATA['_description']}"
    )
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_bratley1992a)  # type: ignore


def evaluate_bratley1992b(xx: np.ndarray) -> np.ndarray:
    """Evaluate the test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    num_dim = xx.shape[1]

    # Compute the function
    ii = np.arange(1, num_dim + 1)
    yy = np.prod(ii * np.cos(ii * xx), axis=1)

    return yy


class Bratley1992b(UQTestFunVarDimABC):
    """An implementation of the test function 2 from Bratley et al. (1992).

    The function (used as an integrand) is a product of a trigonometric
    function.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = (
        f"Integration test function #2 {COMMON_METADATA['_description']}"
    )
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_bratley1992b)  # type: ignore


def evaluate_bratley1992c(xx: np.ndarray) -> np.ndarray:
    """Evaluate the test function #3 of Bratley et al. (1992).

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    num_points, num_dim = xx.shape
    yy = np.ones(num_points)

    # Compute the function
    for m in range(1, num_dim + 1):
        mi = m % 4 + 1
        yy *= eval_chebyt(mi, 2 * xx[:, m - 1] - 1)

    return yy


class Bratley1992c(UQTestFunVarDimABC):
    """An implementation of the test function 3 from Bratley et al. (1992).

    The function (used as an integrand) is a product of a trigonometric
    function.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = (
        f"Integration test function #3 {COMMON_METADATA['_description']}"
    )
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_bratley1992c)  # type: ignore


def evaluate_bratley1992d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    num_points, num_dim = xx.shape
    yy = np.zeros(num_points)

    # Compute the function
    for j in range(num_dim):
        yy += (-1) ** (j + 1) * np.prod(xx[:, : j + 1], axis=1)

    return yy


class Bratley1992d(UQTestFunVarDimABC):
    """An implementation of the test function 4 from Bratley et al. (1992).

    The function (used as an integrand) is a sum of products.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = (
        f"Integration test function #4 {COMMON_METADATA['_description']}"
    )
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_bratley1992d)  # type: ignore
