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


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the speed reducer shaft test function.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 5)`` array of input values.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N``.
        If negative, the system is in failed state.
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
