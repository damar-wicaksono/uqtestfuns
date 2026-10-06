"""
Module with an implementation of the Quadratic RS reliability problem.

The two-dimensional function is a variant of the classic RS reliability problem
with one quadratic term [1].

References
----------
1. Paul Hendrik Waarts, "Structural reliability using finite element
   analysis - an appraisal of DARS: Directional adaptive response surface
   sampling," Civil Engineering and Geosciences, TU Delft, Delft,
   The Netherlands, 2000.
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the quadratic RS function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The performance function of the problem.
        If negative, the system is in failed state.
        The output is a one-dimensional array of length N.
    """
    # Compute the performance function
    yy = xx[:, 0] - xx[:, 1] ** 2

    return yy
