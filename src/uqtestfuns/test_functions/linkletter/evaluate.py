"""
Module with an implementation of the functions from Linkletter et al. (2006)

The paper by Linkletter et al. (2006) [1] contains four nominally analytical
test functions used for sensitivity analysis
in the context of variable selection in Gaussian process metamodeling.
All functions are defined in ten dimensions,
but some (or all) of them are inactive.

Available functions are:

- Linear function with four active input variables.
- Linear function with decreasing coefficients, eight active input variables.
- Inert function without any active input variables.
- Sine function with two active input variables.

References
----------

1. C. Linkletter, D. Bingham, N. Hengartner, D. Higdon, and K. Q. Ye,
   “Variable Selection for Gaussian Process Models in Computer Experiments,”
   Technometrics, vol. 48, no. 4, pp. 478–490, 2006.
   DOI: 10.1198/004017006000000228.
"""

import numpy as np


def linear(xx: np.ndarray) -> np.ndarray:
    """Evaluate the linear function from Linkletter et al. (2006).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 10)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.

    Notes
    -----
    - Only the first four input variables are active; the rest is inactive.
    """
    yy = 0.2 * np.sum(xx[:, :4], axis=1)

    return yy


def dec_coeffs(xx: np.ndarray) -> np.ndarray:
    """Evaluate the linear function with decreasing coefficients.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 10)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.

    Notes
    -----
    - Only the first eight input variables are active; the rest is inactive.
    """
    exps = np.arange(8)  # 8 input variables are active
    coeffs = 0.2 / 2**exps

    yy = np.sum(coeffs * xx[:, :8], axis=1)

    return yy


def inert(xx: np.ndarray) -> np.ndarray:
    """Evaluate the inert function from Linkletter et al. (2006).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 10)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.

    Notes
    -----
    - None of the input variables is active; the function always returns 0.
    """
    yy = np.zeros(xx.shape[0])

    return yy


def sine(xx: np.ndarray) -> np.ndarray:
    """Evaluate the sine function from Linkletter et al. (2006).

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 10)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.

    Notes
    -----
    - Only the first two input variables are active; the rest is inactive.
    """
    yy = np.sin(xx[:, 0]) + np.sin(5 * xx[:, 1])

    return yy
