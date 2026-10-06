"""
Module with an implementation of the simple 3D portfolio model.

The simple portfolio model is a three-dimensional scalar-valued function.
The function was first introduced in [1] as an example for illustrating
different sensitivity measures (i.e., local and hybrid-local).

References
----------

1. A. Saltelli, S. Tarantola, F. Campolongo, M. Rattom, "Sensitivity analysis
   in practice: a guide to assessing scientific models," Hoboken, NJ: Wiley,
   2004.
"""

import numpy as np


def evaluate(xx: np.ndarray, cs: float, ct: float, cj: float) -> np.ndarray:
    """Evaluate the simple portfolio model on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Three-Dimensional input values given by an ``(N, 3)`` array where
        ``N`` is the number of input values.
    cs : float
        The quantities of the portfolio 's' (the most volatile).
    ct : float
        The quantities of the portfolio 't' (average volatility).
    cj : float
        The quantities of the portfolio 'j' (the least volatile).

    Returns
    -------
    np.ndarray
        The output of the simple portfolio model on the given input values.
        The output is a one-dimensional array of length ``N``.
    """
    # Read the parameters
    p = np.array([cs, ct, cj])

    # Compute the simple portfolio model
    yy = np.sum(p * xx, axis=1)

    return yy
