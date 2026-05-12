"""
Module with an implementation of the Sobol-G test function.

The Sobol'-G function is an M-dimensional scalar-valued function.
It was introduced in [1] for testing numerical integration algorithms
(e.g., quasi-Monte-Carlo; see also for instance [2] and [3]).
Its current form (and name) come from [4], where it was generalized
by introducing importance coefficients that control the relative influence
of each input variable.
It has since become a widely used benchmark function
for global sensitivity analysis methods;
see, for instance, [5], [6], [7], and [9].

There are several sets of parameters used in the literature.

Notes
-----
- The parameters used in [5] and [6] correspond to
  parameter choice 3 in [3].

References
----------

1. Paul Bratley, Bennet L. Fox, and Harald Niederreiter, "Implementation and
   tests of low-discrepancy sequences," ACM Transactions on Modeling and
   Computer Simulation, vol. 2, no. 3, pp. 195-213, 1992.
   DOI:10.1145/146382.146385
2. I. Radović, I. M. Sobol’, and R. F. Tichy, “Quasi-Monte Carlo Methods for
   Numerical Integration: Comparison of Different Low Discrepancy Sequences,”
   Monte Carlo Methods and Applications, vol. 2, no. 1, pp. 1–14, 1996.
   DOI: 10.1515/mcma.1996.2.1.1.
3. I. M. Sobol’, “On quasi-Monte Carlo integrations,” Mathematics and Computers
   in Simulation, vol. 47, no. 2–5, pp. 103–112, 1998.
   DOI: 10.1016/S0378-4754(98)00096-2
4. A. Saltelli and I. M. Sobol’, “About the use of rank transformation in
   sensitivity analysis of model output,” Reliability Engineering
   & System Safety, vol. 50, no. 3, pp. 225–239, 1995.
   DOI: 10.1016/0951-8320(95)00099-2.
5. A. Marrel, B. Iooss, F. Van Dorpe, and E. Volkova, “An efficient
   methodology for modeling complex computer codes with Gaussian processes,”
   Computational Statistics & Data Analysis, vol. 52, no. 10,
   pp. 4731–4744, 2008.
   DOI: 10.1016/j.csda.2008.03.026
6. A. Marrel, B. Iooss, B. Laurent, and O. Roustant, “Calculations of Sobol
   indices for the Gaussian process metamodel,” Reliability Engineering &
   System Safety, vol. 94, no. 3, pp. 742–751, 2009.
    DOI: 10.1016/j.ress.2008.07.008
7. S. Kucherenko, B. Feil, N. Shah, and W. Mauntz, “The identification of
   model effective dimensions using global sensitivity analysis,”
   Reliability Engineering & System Safety, vol. 96, no. 4, pp. 440–449, 2011.
   DOI: 10.1016/j.ress.2010.11.003
8. T. Crestaux, J.-M. Martinez, O. Le Maître, and O. Lafitte, “Polynomial
   chaos expansion for uncertainties quantification and sensitivity analysis,”
   presented at the Fifth International Conference on Sensitivity Analysis
   of Model Output, 2007.
   Accessed: Jan. 25, 2023
   URL: http://samo2007.chem.elte.hu/lectures/Crestaux.pdf
9. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np


def get_aa_saltelli1995_1(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to example 1 in [4].

    All input variables are equally important (all coefficients zero).

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = np.zeros(input_dimension)

    return yy


def get_aa_saltelli1995_2(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to example 2 in [4].

    The first two inputs are most important, the third is moderately
    important, and the rest are non-influential.

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
    - Originally, the dimension is limited to 8-dimensions; if more dimensions
      are used, then the remaining dimension is also non-influential.
    """
    yy = np.zeros(input_dimension)

    if input_dimension > 1:
        yy[1] = 0

    if input_dimension > 2:
        yy[2] = 3

    if input_dimension > 3:
        yy[3:] = 9

    return yy


def get_aa_saltelli1995_3(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to example 3 in [4].

    Importance decreases with variable index: the first input is
    the most important and the last is the least important.

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
    - Originally, the dimension is limited to 20-dimensions; if more dimensions
      are used, then the remaining dimension is also non-influential.
    - The parameter set is also used in [8].
    """
    yy = (np.arange(1, input_dimension + 1) - 1) / 2.0

    return yy


def get_aa_sobol1998_1(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to choice 1 in [3].

    The supremum of the Sobol'-G function grows exponentially at 2^M.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = 0.01 * np.ones(input_dimension)

    return yy


def get_aa_sobol1998_2(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to choice 2 in [3].

    The supremum of the Sobol'-G function grows exponentially at 1.5^M.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = np.ones(input_dimension)

    return yy


def get_aa_sobol1998_3(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to choice 3 in [3].

    The supremum of the Sobol'-G function grows linearly at 1 + M/2.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = np.arange(1, input_dimension + 1)

    return yy


def get_aa_sobol1998_4(input_dimension: int) -> np.ndarray:
    """Create importance coefficients Sobol-G according to choice 4 in [3].

    The supremum of the function is bounded at 1.0.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = np.arange(1, input_dimension + 1) ** 2

    return yy


def get_aa_kucherenko2011_2a(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to problem 2A in [7].

    The first two inputs are important, the rest are non-influential.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = np.zeros(input_dimension)
    if input_dimension > 2:
        yy[2:] = 6.52

    return yy


def get_aa_kucherenko2011_3b(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to problem 3B in [7].

    The supremum of the function grows exponentially at 1.13^M.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    yy = 6.52 * np.ones(input_dimension)

    return yy


def get_aa_sun2022(input_dimension: int) -> np.ndarray:
    """Create importance coefficients according to Sec. 3. 2. [9].

    The first four inputs have varying importance; the rest are
    non-influential. Originally defined for M = 7; extrapolated for
    larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of importance coefficients of length ``input_dimension``.
    """
    aa = np.array([0.0, 1.0, 4.5, 9.0, 99, 99, 99])

    if input_dimension > len(aa):
        aa_ext = 99 * np.ones(input_dimension - len(aa))
        aa = np.append(aa, aa_ext)

    return aa[:input_dimension]


def evaluate(xx: np.ndarray, aa: np.ndarray):
    """Evaluate the Sobol'-G function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of importance coefficients of length ``M``; smaller values
        indicate more influential input variables.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.prod(((np.abs(4 * xx - 2) + aa) / (1 + aa)), axis=1)

    return yy
