"""
Module with an implementation of the 1D test func from Forrester et al. (2008).

The function is a one-dimensional multimodal function with a single global
minimum, a local minimum, and a zero-gradient inflection point. It was used
in [1] as a test function for optimization using metamodels.

References
----------

1. Alexander I. J. Forrester, András Sóbester, and Andy J. Keane,
   "Engineering Design via Surrogate Modelling: A Practical Guide,"
   Wiley, 2008.
   DOI: 10.1002/9780470770801
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """The evaluation function for the Forrester et al. (2008) function.

    Parameters
    ----------
    xx : np.ndarray
        One-dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 1D Forrester et al. (2008) function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (6 * xx[:, 0] - 2) ** 2 * np.sin(12 * xx[:, 0] - 4)

    return yy
