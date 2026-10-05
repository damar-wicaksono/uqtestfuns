"""
Module with an implementation of the Friedman test functions.

The Friedman function is a function introduced in [1] as a six-dimensional
(including one dummy variable) test function for testing a spline approximation
method. It was later modified to be a ten-dimensional (including five dummy
variables) function in [2].
In [3], the function was employed as a test function in the context of
sensitivity analysis.

References
----------

1. J. H. Friedman, E. Grosse, and W. Stuetzle, "Multidimensional additive
   spline approximation," SIAM Journal on Scientific and Statistical Computing,
   vol. 4, no. 2, pp. 291-301, 1983.
2. J. H. Friedman, "Multivariate adaptive regression splines," The Annals of
   Statistics, vol. 19, no. 1, pp. 1-67, 1991.
   DOI: 10.1214/aos/1176347963
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental
   Modelling & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Friedman test function.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``M`` >= 6 and
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Friedman function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.

    Notes
    -----
    - Only the first five input variables are active; the rest is inactive.
    """
    yy_1 = 10 * np.sin(np.pi * xx[:, 0] * xx[:, 1])
    yy_2 = 20 * (xx[:, 2] - 0.5) ** 2
    yy_3 = 10 * xx[:, 3]
    yy_4 = 5 * xx[:, 4]

    return yy_1 + yy_2 + yy_3 + yy_4
