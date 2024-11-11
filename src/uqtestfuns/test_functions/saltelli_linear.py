"""
Module with an implementation of the linear fun. from Saltelli et al. (2008).

The linear function from Saltelli et al. (2008) is an M-dimensional
scalar-valued function.
It was introduced in [1] to illustrate sensitivity analysis methods and used
in [2] for benchmarking purposes.

Due to its simple structure, its moments and Sobol' sensitivity indices can
be computed analytically.

References
----------
1. A. Saltelli, K. Chan, and E. Scott, 2008. Sensitivity Analysis: Wiley Series
   in Probability and Statistics. Wiley, New York.
2. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from uqtestfuns.core.custom_typing import (
    MarginalSpec,
    MarginalSpecs,
    ProbInputSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["SaltelliLinear"]


def _create_marginals(input_dimension: int) -> MarginalSpecs:
    r"""Create a list of marginal specifications of the given dimension.

    .. math::

      X_i \sim \mathcal{U}[x_{o, i} - \sigma_{o, i}, x_{o, i} + \sigma_{o, i}]

    where :math:`x_{o, i} = 3^{i - 1}` and :math:`\sigma_{o, i} = 0.5 x_{o, i}`
    for :math:`i = 1, 2, \ldots`.

    Parameters
    ----------
    input_dimension : int
        The number of marginal specifications in the list.

    Returns
    -------
    MarginalSpecs
        The list of marginal specifications.
    """
    marginals = []
    for i in range(input_dimension):
        mid = 3**i
        delta = 0.5 * mid
        marginal: MarginalSpec = {
            "name": f"X{i + 1}",
            "distribution": "uniform",
            "parameters": [mid - delta, mid + delta],
            "description": None,
        }
        marginals.append(marginal)

    return marginals


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Saltelli2000": {
        "function_id": "SaltelliLinear",
        "description": (
            "Probabilistic input model for the linear function "
            "from Saltelli et al. (2000)"
        ),
        "marginals": _create_marginals,
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray):
    """Evaluate the linear function on a set of input values.

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
    yy = np.sum(xx, axis=1)

    return yy


class SaltelliLinear(UQTestFunVarDimABC):
    """An implementation of the M-dimensional Saltelli linear function."""

    _tags = ["sensitivity"]
    _description = "Linear function from Saltelli et al. (2000)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
