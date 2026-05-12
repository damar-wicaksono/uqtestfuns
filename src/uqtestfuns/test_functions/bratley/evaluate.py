"""
Module with an implementation of the Bratley et al. (1992) test functions.

The Bratley et al. (1992) paper [1] contains four M-dimensional scalar-valued
functions for testing multidimensional numerical integrations using
low-discrepancy sequences. The functions were used in [2] and [3]
in the context of global sensitivity analysis.

The BratleyD function may also be referred to as the "Bratley function"
or "Bratley et al. (1992) function" in the literature.

References
----------

1. Paul Bratley, Bennet L. Fox, and Harald Niederreiter, "Implementation and
   tests of low-discrepancy sequences," ACM Transactions on Modeling and
   Computer Simulation, vol. 2, no. 3, pp. 195-213, 1992.
   DOI:10.1145/146382.146385
2. S. Kucherenko, M. Rodriguez-Fernandez, C. Pantelides, and N. Shah,
   “Monte Carlo evaluation of derivative-based global sensitivity measures,”
   Reliability Engineering & System Safety, vol. 94, pp. 1137–1148, 2009.
   DOI:10.1016/j.ress.2008.05.006
3. A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto,
   and S. Tarantola, “Variance based sensitivity analysis of model output.
   Design and estimator for the total sensitivity index,” Computer Physics
   Communications, vol. 181, no. 2, pp. 259–270, 2010,
   DOI:10.1016/j.cpc.2009.09.018
"""

import numpy as np

from scipy.special import eval_chebyt


def bratley_a(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Bratley et al. (1992) A function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    return np.prod(np.abs(4.0 * xx - 2.0), axis=1)


def bratley_b(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Bratley et al. (1992) B function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """

    num_dim = xx.shape[1]

    # Compute the function
    ii = np.arange(1, num_dim + 1)
    yy = np.prod(ii * np.cos(ii * xx), axis=1)

    return yy


def bratley_c(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Bratley et al. (1992) C function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.

    Notes
    -----
    - This function requires ``scipy.special.eval_chebyt``.
    """

    num_points, num_dim = xx.shape
    yy = np.ones(num_points)

    # Compute the function
    for m in range(1, num_dim + 1):
        mi = m % 4 + 1
        yy *= eval_chebyt(mi, 2 * xx[:, m - 1] - 1)

    return yy


def bratley_d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Bratley et al. (1992) D function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """

    num_points, num_dim = xx.shape
    yy = np.zeros(num_points)

    # Compute the function
    for j in range(num_dim):
        yy += (-1) ** (j + 1) * np.prod(xx[:, : j + 1], axis=1)

    return yy
