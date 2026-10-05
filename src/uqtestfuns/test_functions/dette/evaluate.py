"""
Module with an implementation of the functions from Dette and Pepelyshev (2010)

The paper by Dette and Pepelyshev [1] contains several analytical test
functions used to compare different experimental designs for metamodeling
applications.

References
----------

1. H. Dette and A. Pepelyshev, “Generalized Latin Hypercube Design for Computer
   Experiments,” Technometrics, vol. 52, no. 4, pp. 421–429, 2010.
   DOI: 10.1198/TECH.2010.09157.
"""

import numpy as np


def curved(xx: np.ndarray) -> np.ndarray:
    """Evaluate the highly-curved function from Dette and Pepelyshev (2010).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 3)`` array of input values,
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.
    """
    term_1 = 4 * (xx[:, 0] - 2 + 8 * xx[:, 1] - 8 * xx[:, 1] ** 2)
    term_2 = (3 - 4 * xx[:, 1]) ** 2
    term_3 = (16 * (xx[:, 2] + 1) ** 0.5) * (2 * xx[:, 2] - 1) ** 2

    return term_1 + term_2 + term_3


def exp(xx: np.ndarray) -> np.ndarray:
    """Evaluate the exponential function from Dette and Pepelyshev (2010).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 3)`` array of input values,
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.
    """
    yy = np.sum(np.exp(-2 / xx ** ([1.75, 1.5, 1.25])), axis=1)

    return 100 * yy


def eight_d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 8D function from Dette and Pepelyshev (2010).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 8)`` array of input values,
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.
    """
    term_1 = curved(xx)
    term_2 = np.zeros(len(xx))
    for j in range(3, xx.shape[1]):
        term_2 += (j + 1) * np.log(1 + np.sum(xx[:, 2:j], axis=1))

    return term_1 + term_2
