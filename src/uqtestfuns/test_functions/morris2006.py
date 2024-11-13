"""
This module implements the Morris function from Morris et al. (2006).

The Morris function is an M-dimensional, scalar-valued function commonly used
as a test function for sensitivity analysis.
It was first appeared in [1] and it has been revisited multiple times in the
literature in similar contexts, e.g., [2], [3].

The function features a parameter that dictates the number of important
input variables. The remaining input variables are inert. Furthermore,
all sensitivity indices of the important variables have
the same Sobol' sensitivity indices.

References
----------

1. M. D. Morris, L. M. Moore, and M. D. McKay, “Sampling plans based on
   balanced incomplete block designs for evaluating the importance of
   computer model inputs,” Journal of Statistical Planning and Inference,
   vol. 136, no. 9, pp. 3203–3220, 2006.
   DOI: 10.1016/j.jspi.2005.01.001
2. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
3. A. Horiguchi, M. T. Pratola, and T. J. Santner, “Assessing variable activity
   for Bayesian regression trees,” Reliability Engineering & System Safety,
   vol. 207, p. 107391, 2021,
   DOI: 10.1016/j.ress.2020.107391
"""

import numpy as np

from uqtestfuns.core.custom_typing import FunParamSpecs, ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["Morris2006"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Morris2006": {
        "function_id": "Morris2006",
        "description": (
            "Probabilistic input model for the M-dimensional function "
            "from Morris et al. (2006)"
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


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Morris2006": {
        "function_id": "Morris2006",
        "description": (
            "Parameter set for the M-dimensional function from "
            "Morris et al. (2006); the parameter controls the number of "
            "important input variables"
        ),
        "declared_parameters": [
            {
                "keyword": "p",
                "value": 10,
                "type": int,
                "description": "# of important inputs",
            },
        ],
    }
}


def evaluate(xx: np.ndarray, p: int) -> np.ndarray:
    """Evaluate the Morris2006 test function.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    p : int
        The number of important input variables. If p > M then p is set
        equal to M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    input_dim = xx.shape[1]
    if p > input_dim:
        p = input_dim

    alpha = np.sqrt(12) - 6 * np.sqrt(0.1 * (p - 1))

    term_1 = alpha * np.sum(xx[:, :p], axis=1)
    if p == 1:
        return term_1

    beta = 12 / np.sqrt(10 * (p - 1))
    term_2 = np.zeros(len(xx))
    for i in range(p - 1):
        ip1 = i + 1
        term_2[:] += xx[:, i] * np.sum(xx[:, ip1:p], axis=1)
    term_2 *= beta

    yy = term_1 + term_2

    return yy


class Morris2006(UQTestFunVarDimABC):
    """An implementation of the M-dimensional Morris2006."""

    _tags = ["sensitivity"]
    _description = "Test function from Morris et al. (2006)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS

    evaluate = staticmethod(evaluate)  # type: ignore
