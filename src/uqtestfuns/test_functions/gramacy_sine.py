"""
Module with an implementation of the 1D Gramacy (2007) test function.

The Gramacy (2007) one-dimensional sine function is a scalar-valued function
that features two regimes: one part is a mixture of sine and cosine and
another part is a linear function. The function was introduced in [1]
as a test function for non-stationary Gaussian process metamodeling
by partitioning the input parameter space.

In the original paper the response is disturbed
by i.i.d. Gaussian noise eps ~ N(0, 0.1).

References
----------

1. Robert B. Gramacy, “tgp: An R Package for Bayesian nonstationary,
   semiparametric nonlinear regression and design by Treed Gaussian Process
   models,” Journal of Statistical Software, vol. 19, no. 9, 2007.
   DOI: 10.18637/jss.v019.i09.
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 1D Gramacy (2007) Sine function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.
    parameters : Generator, optional
        A random number generator to generate the noise.

    Returns
    -------
    np.ndarray
        The output of the 1D Gramacy (2007) function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.zeros(len(xx))
    idx_1 = xx[:, 0] <= 9.6
    idx_2 = xx[:, 0] > 9.6
    yy[idx_1] = np.sin(0.2 * np.pi * xx[idx_1, 0]) + 0.2 * np.cos(
        0.8 * np.pi * xx[idx_1, 0]
    )
    yy[idx_2] = -1 + 0.1 * xx[idx_2, 0]

    return yy
