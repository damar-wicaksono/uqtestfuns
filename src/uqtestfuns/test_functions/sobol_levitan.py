"""
This module implements the Sobol'-Levitan test function.

The Sobol'-Levitan function is an M-dimensional, scalar-valued function
commonly used as a benchmark for sensitivity analysis.
The function was introduced in [1] (as a six- and 20-dimensional functions)
and revisited in, for example, [2] (as a 20-dimensional function)
and [3] (as a seven- and 15-dimensional functions).

The Sobol' sensitivity indices of the test function can be derived analytically
as functions of the parameter.

References
----------

1. I. M. Sobol’ and Yu. L. Levitan, “On the use of variance reducing
   multipliers in Monte Carlo computations of a global sensitivity index,”
   Computer Physics Communications, vol. 117, no. 1–2, pp. 52–61, 1999.
   DOI: 10.1016/S0010-4655(98)00156-8
2. H. Moon, A. M. Dean, and T. J. Santner, “Two-Stage Sensitivity-Based Group
   Screening in Computer Experiments,” Technometrics*, vol. 54, no. 4,
   pp. 376–387, 2012.
   DOI: 10.1080/00401706.2012.725994
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np


def get_bb_sobol1999_1(input_dimension: int) -> np.ndarray:
    """Create importance coefficients Sobol' and Levitan (1999) example 6.1.

    Originally defined for M = 6. Truncated for smaller dimensions;
    extrapolated with 0.9 for larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    bb = np.array([1.5, 0.9, 0.9, 0.9, 0.9, 0.9])

    if input_dimension > 6:
        bb_ext = 0.9 * np.ones(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


def get_bb_sobol1999_2(input_dimension: int) -> np.ndarray:
    """Create importance coefficients Sobol' and Levitan (1999) example 6.2.

    Originally defined for M = 20. Truncated for smaller dimensions;
    extrapolated with 0.4 for larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    bb_1 = 0.6 * np.ones(10)
    bb_2 = 0.4 * np.ones(10)
    bb = np.append(bb_1, bb_2)

    if input_dimension > 20:
        bb_ext = 0.4 * np.ones(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


def get_bb_moon2012_1(input_dimension: int) -> np.ndarray:
    """Create importance coefficients for Moon et al. (2012) base case.

    Originally defined for M = 20 in [2]. Truncated for smaller dimensions;
    extrapolated with 0.0 for larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    bb = np.array(
        [
            2.0000,
            1.9500,
            1.9000,
            1.8500,
            1.8000,
            1.7500,
            1.7000,
            1.6500,
            0.4228,
            0.3077,
            0.2169,
            0.1471,
            0.0951,
            0.0577,
            0.0323,
            0.0161,
            0.0068,
            0.0021,
            0.0004,
            0.0000,
        ]
    )

    if input_dimension > 20:
        bb_ext = np.zeros(input_dimension - len(bb))
        bb = np.append(bb, bb_ext)

    return bb[:input_dimension]


def evaluate(xx: np.ndarray, bb: np.ndarray, c0: float) -> np.ndarray:
    """Evaluate the Sobol'-Levitan function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    bb : np.ndarray
        An array of importance coefficients of length ``M``; larger values
        indicate more influential input variables.
    c0 : float
        Constant shift term; affects the mean but not the sensitivity indices.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.

    Notes
    -----
    - When ``bb[i] == 0``, the term ``(exp(b) - 1) / b`` is singular but
      its limit as ``b -> 0`` is ``1.0``, which is used instead.
    """
    input_dim = xx.shape[1]
    ii = 1.0
    for i in range(input_dim):
        b = bb[i]
        # Safeguard against zero-value coefficient
        if b == 0:
            ii *= 1.0  # the limit as b approaches 0
        else:
            ii *= (np.exp(b) - 1) / b

    yy = np.exp(np.sum(bb * xx, axis=1)) - ii + c0

    return yy
