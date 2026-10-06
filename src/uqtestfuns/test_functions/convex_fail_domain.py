"""
Module with an implementation of the convex failure domain problem.

The two-dimensional function is a reliability analysis problem used,
for instance, in [1] and [2].

References
----------
1. A. Borri and E. Speranzini, “Structural reliability analysis using a
   standard deterministic finite element code,” Structural Safety, vol. 19,
   no. 4, pp. 361–382, 1997. DOI: 10.1016/S0167-4730(97)00017-9
2. Paul Hendrik Waarts, “Structural reliability using finite element
   analysis - an appraisal of DARS: Directional adaptive response surface
   sampling," Civil Engineering and Geosciences, TU Delft, Delft,
   The Netherlands, 2000.
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the convex failure domain function on a set of input values.

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
    yy = (
        0.1 * (xx[:, 0] - xx[:, 1]) ** 2
        - (xx[:, 0] + xx[:, 1]) / np.sqrt(2)
        + 2.5
    )

    return yy
