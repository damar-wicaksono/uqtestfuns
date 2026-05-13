"""
Module with an implementation of the Modified Sobol-G test function.

The Sobol'-G* function is an M-dimensional scalar-valued function that first
appeared in [1] as a modification of the original Sobol'-G function [2].
It introduces shift and curvature parameters to the original formulation
to avoid a discontinuity at the mid-point of the domain. It has been used
as a benchmark for sensitivity analysis methods in [3] and [4].

There are several sets of parameters used in the literature.

References
----------

1. A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto,
   and S. Tarantola, “Variance based sensitivity analysis of model output.
   Design and estimator for the total sensitivity index,”
   Computer Physics Communications, vol. 181, no. 2, pp. 259–270, 2010.
   DOI: 10.1016/j.cpc.2009.09.018
2. A. Saltelli and I. M. Sobol’, “About the use of rank transformation in
   sensitivity analysis of model output,” Reliability Engineering
   & System Safety, vol. 50, no. 3, pp. 225–239, 1995.
   DOI: 10.1016/0951-8320(95)00099-2.
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
4. I. Azzini and R. Rosati, "Sobol' main effect index: an Innovative
   Algorithm (IA) using Dynamic Adaptive Variances," Reliability
   Engineering & System Safety, vol. 213, p. 107647, 2021.
   DOI: 10.1016/j.ress.2021.107647
"""

import numpy as np


def get_aa_saltelli2010_a(input_dimension: int) -> np.ndarray:
    """Create importance coefficients for Saltelli et al. (2010) variant A.

    Used in test cases 1, 3, 5 in [1] and in [4]. The first two inputs are
    the most important; the rest are non-influential.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.

    Notes
    -----
    - In [1] and in [4], an input dimension of 10 was used.
      If the input dimension is less than 10, the parameter array is truncated;
      if the input dimension exceeds 10, the parameters are extrapolated.
    """
    aa = 9.0 * np.ones(input_dimension)
    aa[:2] = 0.0

    return aa


def get_aa_saltelli2010_b(input_dimension: int) -> np.ndarray:
    """Create importance coefficients for Saltelli et al. (2010) variant B.

    Used in test cases 2, 4, and 6. Importance decreases with variable
    index. Originally defined for M = 10; extrapolated for larger
    dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    aa = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1, 2, 3, 4])

    if input_dimension > 10:
        aa_ext = np.arange(5, input_dimension - 5)
        aa = np.append(aa, aa_ext)

    return aa[:input_dimension]


def get_alpha_saltelli2010_a(input_dimension: int) -> np.ndarray:
    """Create curvature parameters for Saltelli et al. (2010) variant A.

    Used in test cases 1 and 2 (see Table 5 in [1]).
    All curvature parameters equal 1.0 (linear terms).

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of curvature parameters of length ``input_dimension``.

    Notes
    -----
    - In [1] and in [4], an input dimension of 10 was used.
      If the input dimension is less than 10, the parameter array is truncated;
      if the input dimension exceeds 10, the parameters are extrapolated.
    """
    alpha = np.ones(input_dimension)

    return alpha


def get_alpha_saltelli2010_b(input_dimension: int) -> np.ndarray:
    """Create curvature parameters for Saltelli et al. (2010) variant B.

    Used in test cases 3 and 4 from [1] (see Table 5), and in [4].
    All curvature parameters equal 0.5 (concave terms).

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of curvature parameters of length ``input_dimension``.

    Notes
    -----
    - In [1] and in [4], an input dimension of 10 was used.
      If the input dimension is less than 10, the parameter array is truncated;
      if the input dimension exceeds 10, the parameters are extrapolated.
    """
    alpha = 0.5 * np.ones(input_dimension)

    return alpha


def get_alpha_saltelli2010_c(input_dimension: int) -> np.ndarray:
    """Create curvature parameters for Saltelli et al. (2010) variant C.

    Used in test cases 5 and 6 (see Table 5 in [1]).
    All curvature parameters equal 2.0 (convex terms).

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of curvature parameters of length ``input_dimension``.

    Notes
    -----
    - In [1], an input dimension of 10 was used. If the input dimension
      is less than 10, the parameter array is truncated; if the input dimension
      exceeds 10, the parameters are extrapolated.
    """
    alpha = 2 * np.ones(input_dimension)

    return alpha


def get_delta_saltelli2010(input_dimension: int) -> np.ndarray:
    """Create shift parameters for Saltelli et al. (2010).

    The shift parameters are randomly drawn from a uniform distribution
    over [0, 1] at instantiation time and fixed for the lifetime of the
    instance, following the prescription in [1]. This randomness is a
    property of the Saltelli et al. (2010) parameterization,
    not the function itself; delta cancels out in the computation of moments
    and sensitivity indices.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of shift parameters of length ``input_dimension``.
    """
    rng = np.random.default_rng()
    delta = rng.random(input_dimension)

    return delta


def get_delta_azzini2021(input_dimension: int) -> np.ndarray:
    """Create shift parameters for Azzini and Rosati (2021).

    All shift parameters are fixed at 0.5, following Section 3.2.2 in [4].
    This is a deterministic alternative to the randomly generated delta
    in the Saltelli parameterization; delta cancels out in the computation
    of moments and sensitivity indices regardless of its value.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of shift parameters of length ``input_dimension``.
    """
    return 0.5 * np.ones(input_dimension)


def evaluate(
    xx: np.ndarray,
    aa: np.ndarray,
    delta: np.ndarray,
    alpha: np.ndarray,
) -> np.ndarray:
    """Evaluate the Sobol'-G* function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of importance coefficients of length ``M``; smaller values
        indicate more influential input variables.
    delta : np.ndarray
        An array of shift parameters of length ``M``; cancels in moments
        and sensitivity indices.
    alpha : np.ndarray
        An array of curvature parameters of length ``M``; values less than
        1.0 give concave terms, greater than 1.0 give convex terms.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function
        output.
    """
    term = np.abs(2 * (xx + delta - np.floor(xx + delta)) - 1) ** alpha
    g_star = ((1 + alpha) * term + aa) / (1 + aa)

    yy = np.prod(g_star, axis=1)

    return yy
