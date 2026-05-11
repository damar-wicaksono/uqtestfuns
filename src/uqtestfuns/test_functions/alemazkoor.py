"""
Module with an implementation of Alemazkoor & Meidani (2008) test functions.

There are two test functions from [1].
One features a low-dimensional polynomial function with a high degree
(a total degree of 20).

The functions were used as test functions
for a metamodeling exercise (i.e., sparse polynomial chaos expansion) in [1].

References
----------

1. Negin Alemazkoor and Hadi Meidani, "A near-optimal sampling strategy for
   sparse recovery of polynomial chaos expansions," Journal of Computational
   Physics, vol. 371, pp. 137-151, 2018.
   DOI: 10.1016/j.jcp.2018.05.025
"""

import numpy as np


def evaluate_2d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 2D test function from Alemazkoor & Meidani (2018).

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an ``(N, 2)`` array where
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a one-dimensional array of length ``N``.
    """
    yy = np.zeros(xx.shape[0])

    for i in range(1, 6):
        yy += xx[:, 0] ** (2 * i) * xx[:, 1] ** (2 * i)

    return yy


def evaluate_20d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 20D test function from Alemazkoor & Meidani (2018).

    Parameters
    ----------
    xx : np.ndarray
        A 20-dimensional input values given by an ``(N, 20)`` array
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a one-dimensional array of length ``N``.
    """
    yy = np.sum(xx[:, :-1] * xx[:, 1:], axis=1)

    return yy
