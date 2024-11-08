"""
Module with an implementation of the speed reducer shaft test function.

The speed reducer shaft test function is a five-dimensional scalar-valued
test function introduced in [1]. It is used as a test function for reliability
analysis algorithms (see, for instance, [1], [2]).

The function models the performance of a shaft in a speed reducer.
The performance is defined as the strength of the shaft subtracted by the
stress. If the value is negative, then the system is in failed state.

References
----------
1. Xiaoping Du and Agus Sudjianto, “First order saddlepoint approximation
   for reliability analysis,” AIAA Journal, vol. 42, no. 6, pp. 1199–1207,
   2004.
   DOI: 10.2514/1.3877
2. X. Li, C. Gong, L. Gu, W. Gao, Z. Jing, and H. Su, “A sequential surrogate
   method for reliability analysis based on radial basis function,”
   Structural Safety, vol. 73, pp. 42–53, 2018.
   DOI: 10.1016/j.strusafe.2018.02.005
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC
from .utils import gumbel_max_mu, gumbel_max_beta

__all__ = ["SpeedReducerShaft"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Du2004": {
        "function_id": "SpeedReducerShaft",
        "description": (
            "Input model for the speed reducer shaft problem "
            "from Du and Sudjianto (2004)"
        ),
        "marginals": [
            {
                "name": "D",
                "distribution": "normal",
                "parameters": [39, 0.1],
                "description": "Shaft diameter [mm]",
            },
            {
                "name": "L",
                "distribution": "normal",
                "parameters": [400, 0.1],
                "description": "Shaft span [mm]",
            },
            {
                "name": "F",
                "distribution": "gumbel",
                "parameters": [gumbel_max_mu(1500, 350), gumbel_max_beta(350)],
                "description": "External force [N]",
            },
            {
                "name": "T",
                "distribution": "normal",
                "parameters": [250, 35],
                "description": "Torque [Nm]",
            },
            {
                "name": "S",
                "distribution": "uniform",
                "parameters": [70, 80],
                "description": "Strength [MPa]",
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the speed reducer shaft test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A five-dimensional input values given by N-by-5 arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the speed reducer shaft test function.
        If negative, then the system is in failed state.
        The output is a one-dimensional array of length N.
    """
    dd = xx[:, 0]  # diameter [mm]
    ll = xx[:, 1]  # span [mm]
    ff = xx[:, 2]  # external force [N]
    tt = xx[:, 3]  # torque [Nm]
    ss = xx[:, 4]  # strength [MPa]

    # NOTE: Convert [MPa] to [Pa] and [mm] to [m]
    yy = ss * 1e6 - (32 / np.pi / (dd / 1e3) ** 3) * np.sqrt(
        ff**2 * (ll / 1e3) ** 2 / 16 + tt**2
    )

    return yy


class SpeedReducerShaft(UQTestFunFixDimABC):
    """A concrete implementation of the speed reducer shaft function."""

    _tags = ["reliability"]
    _description = (
        "Reliability of a shaft in a speed reducer "
        "from Du and Sudjianto (2004)"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
