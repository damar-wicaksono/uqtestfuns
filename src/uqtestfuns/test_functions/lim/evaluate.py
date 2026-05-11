"""
Module with implementations of the two functions from Lim et al. (2002).

The test functions are two-dimensional scalar-valued functions used in [1]
to illustrate the connection between Gaussian process metamodels and
polynomials.

References
----------

1. Y. B. Lim, J. Sacks, W. J. Studden, and W. J. Welch, “Design and analysis of
   computer experiments when the output is highly correlated over the input
   space,” Canadian Journal of Statistics, vol. 30, no. 1, pp. 109–126, 2002,
   DOI: 10.2307/3315868
"""

import numpy as np


def poly(xx: np.ndarray) -> np.ndarray:
    """Evaluate the polynomial test function from Lim et al (2002).

    The function is a polynomial with a maximum total degree of 5.

    Parameters
    ----------
    xx : np.ndarray
        An (``N``, 2) array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    trm_1 = 5.0 / 2.0 * xx[:, 0]
    trm_2 = 35.0 / 2.0 * xx[:, 1]
    trm_3 = 5.0 / 2.0 * xx[:, 0] * xx[:, 1]
    trm_4 = 19 * xx[:, 1] ** 2
    trm_5 = 15.0 / 2.0 * xx[:, 0] ** 3
    trm_6 = 5.0 / 2.0 * xx[:, 0] * xx[:, 1] ** 2
    trm_7 = 11.0 / 2.0 * xx[:, 1] ** 4
    trm_8 = xx[:, 0] ** 3 * xx[:, 1] ** 2

    yy = 9 + trm_1 - trm_2 + trm_3 + trm_4 - trm_5 - trm_6 - trm_7 + trm_8

    return yy


def non_poly(xx: np.ndarray) -> np.ndarray:
    """Evaluate the non-polynomial test function from Lim et al (2002).

    Parameters
    ----------
    xx : np.ndarray
        An (``N``, 2) array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    trm_1 = 30 + 5 * xx[:, 0] * np.sin(5 * xx[:, 0])
    trm_2 = 4 + np.exp(-5 * xx[:, 1])

    yy = (trm_1 * trm_2 - 100) / 6.0

    return yy
