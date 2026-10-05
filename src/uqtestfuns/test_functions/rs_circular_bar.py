"""
Module with an implementation of the circular bar RS problem.

The two-dimensional reliability problem is a variant of the classic RS
reliability problem in the context of a carbon-steel circular bar subjected
to an axial force, introduced in [1].

References
----------
1. A. K. Verma, S. Ajit, and D. R. Karanki, “Structural Reliability,”
   in Reliability and Safety Engineering, in Springer Series
   in Reliability Engineering. London: Springer London, 2016, pp. 257–292.
   DOI: 10.1007/978-1-4471-6269-8_8
"""

import numpy as np


def evaluate(xx: np.ndarray, bar_diameter: float) -> np.ndarray:
    """Evaluate the circular bar RS problem on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An array of shape ``(N, 2)`` where ``N`` is the number of input values.
    bar_diameter : float
        The diameter of the bar in [mm].

    Returns
    -------
    np.ndarray
        The performance function of the problem.
        If negative, the system is in a failed state.
        The output is a one-dimensional array of length ``N``.
    """
    # --- Convert to SI units
    # Yield strength: [MPa] to [Pa]
    yy_ = xx[:, 0] * 1e6
    # Axial force: [kN] to [N]
    ff = xx[:, 1] * 1e3
    # Diameter: [mm] to [m]
    diam = bar_diameter * 1e-3

    # Compute the performance function
    yy = yy_ - ff / (np.pi * diam**2 / 4)

    return yy
