"""
Module with an implementation of the Wing Weight test function.

The Wing Weight test function [1] is a 10-dimensional scalar-valued function
that models a light aircraft wing.
The function has been used as a test function in the context of
metamodeling [2] and optimization [1].

References
----------

1. Alexander I. J. Forrester, András Sóbester, and Andy J. Keane,
   Engineering Design via Surrogate Modelling: A Practical Guide, 1st ed.
   Wiley, 2008.
   DOI: 10.1002/9780470770801.
2. Lavi R. Zuhal, Kemas Zakaria, Pramudita S. Palar, Koji Shimoyama,
   and Rhea P. Liem, "Gradient-enhanced universal Kriging with polynomial
   chaos as trend function," In AIAA Scitech 2020 Forum,
   Orlando, Florida, 2020. American Institute of Aeronautics and Astronautics.
   DOI: 10.2514/6.2020-1865.
"""

import numpy as np

from .utils import deg2rad


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Wing Weight function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 10)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Wing Weight function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.
    """
    # Compute the Wing Weight function
    term_1 = 0.036 * xx[:, 0] ** 0.758 * xx[:, 1] ** 0.0035
    term_2 = (xx[:, 2] / np.cos(deg2rad(xx[:, 3])) ** 2) ** 0.6
    term_3 = xx[:, 4] ** 0.006
    term_4 = xx[:, 5] ** 0.04
    term_5 = (100 * xx[:, 6] / np.cos(np.pi / 180.0 * xx[:, 3])) ** (-0.3)
    term_6 = (xx[:, 7] * xx[:, 8]) ** 0.49
    term_7 = xx[:, 0] * xx[:, 9]

    yy = term_1 * term_2 * term_3 * term_4 * term_5 * term_6 + term_7

    return yy
