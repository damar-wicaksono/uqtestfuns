"""
This module provides an implementation of the Rosenbrock function.

The Rosenbrock function, originally introduced in [1] as a two-dimensional
scalar-valued test function for global optimization, was later generalized
to M dimensions.
It has since become a widely used benchmark for global optimization methods
(e.g., [2], [3]).
In [4], the function was employed in a metamodeling exercise.

The function features a curved, non-convex valley.
While it is relatively easy to reach the valley, the convergence to the global
minimum is challenging.

References
----------
1. H. H. Rosenbrock, “An Automatic Method for Finding the Greatest or Least
   Value of a Function,” The Computer Journal, vol. 3, no. 3, pp. 175–184,
   1960.
   DOI: 10.1093/comjnl/3.3.175
2. L. C. W. Dixon and G. P. Szegö. Towards global optimization 2,
   chapter The global optimization problem: an introduction, pages 1–15.
   North-Holland, Amsterdam, 1978.
3. V. Picheny, T. Wagner, and D. Ginsbourger, “A benchmark of kriging-based
   infill criteria for noisy optimization,” Structural and Multidisciplinary
   Optimization, vol. 48, no. 3, pp. 607–626, 2013.
   DOI: 10.1007/s00158-013-0919-4
4. M. H. Y. Tan, “Stochastic Polynomial Interpolation for Uncertainty
   Quantification With Computer Experiments,” Technometrics, vol. 57, no. 4,
   pp. 457–467, 2015.
   DOI: 10.1080/00401706.2014.950431
"""

import numpy as np


def evaluate(
    xx: np.ndarray,
    a: float,
    b: float,
    c: float,
    d: float,
) -> np.ndarray:
    """Evaluate the Rosenbrock function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    a : float
        Parameter controlling the location of the global optimum.
    b : float
        Parameter controlling the steepness and width of the valley.
    c : float
        Shift parameter.
    d : float
        Scale parameter.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    # Deal with special dimension of 1
    if xx.shape[1] == 1:
        yy = (xx[:, 0] - a) ** 2
    else:
        yy = (xx[:, :-1] - a) ** 2 + b * (xx[:, 1:] - xx[:, :-1] ** 2) ** 2
        yy = np.sum(yy, axis=1)

    # Shift and rescale
    yy = (yy - c) / d

    return yy
