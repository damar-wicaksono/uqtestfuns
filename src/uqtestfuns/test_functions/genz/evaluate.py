"""
Module with implementations of integral test functions from Genz (1984).

Genz [1] introduced six challenging parameterized M-dimensional functions
designed to test the performance of numerical integration routines:

- Oscillatory function features an oscillating shape in the multidimensional
  space.
- Product peak function features a prominent peak at the center
  of the multidimensional space.
- Corner peak function features a prominent peak in one corner
  of the multidimensional space. This function was featured as a test function
  in sensitivity analysis [2] and metamodeling [3] exercises.
- Gaussian function features a bell-shaped peak at the center
  of the multidimensional space.
- Continuous function features an exponential decay from the center
  of the multidimensional space. The function is continuous everywhere,
  but non-differentiable at the center.
- Discontinuous function features an exponential rise from a corner
  of the multidimensional space up to the offset parameter value,
  after which the function value drops to zero everywhere,
  creating discontinuity. This function was featured as a test function
  in sensitivity analysis [2].

The functions are further characterized by shape and offset parameters.
While the shift parameter has minimal impact on the integral's value,
the scale parameter significantly affects the difficulty
of the integration problem.

References
----------

1. A. Genz, “Testing Multidimensional Integration Routines,”
   in Proc. of International Conference on Tools, Methods and Languages
   for Scientific and Engineering Computation, USA: Elsevier North-Holland,
   Inc., 1984, pp. 81–94.
2. X. Zhang and M. D. Pandey, “An effective approximation for variance-based
   global sensitivity analysis,” Reliability Engineering & System Safety,
   vol. 121, pp. 164–174, 2014.
   DOI: 10.1016/j.ress.2013.07.010
3. J. D. Jakeman, M. S. Eldred, and K. Sargsyan, “Enhancing l1-minimization
   estimates of polynomial chaos expansions using basis selection,”
   Journal of Computational Physics, vol. 289, pp. 18–34, 2015.
   DOI: 10.1016/j.jcp.2015.02.025.
"""

import numpy as np


def get_aa_genz1984(input_dimension: int) -> np.ndarray:
    """Create shape parameters for the Genz (1984) family [1].

    All shape parameters are set to 5.0.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of shape parameters of length ``input_dimension``.
    """
    aa = 5.0 * np.ones(input_dimension)

    return aa


def get_bb_genz1984(input_dimension: int) -> np.ndarray:
    """Create offset parameters for the Genz (1984) family [1].

    All offset parameters are set to 0.5.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of offset parameters of length ``input_dimension``.
    """
    bb = 0.5 * np.ones(input_dimension)

    return bb


def get_aa_zhang2014_1(input_dimension: int) -> np.ndarray:
    """Create shape parameters for Zhang and Pandey (2014) case 1 [2].

    Linearly increasing from 0.02, originally defined for M = 3;
    extrapolated for larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of shape parameters of length ``input_dimension``.

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    """
    aa = 0.02 + 0.03 * np.arange(input_dimension)

    return aa


def get_aa_zhang2014_2(input_dimension: int) -> np.ndarray:
    """Create shape parameters for Zhang and Pandey (2014) case 2 [2].

    Linearly increasing by 0.1, originally defined for M = 10;
    extrapolated for larger dimensions.

    Parameters
    ----------
    input_dimension : int
        The number of input variables.

    Returns
    -------
    np.ndarray
        An array of shape parameters of length ``input_dimension``.

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    """
    aa = 0.1 * np.arange(1, input_dimension + 1)

    return aa


def continuous(xx: np.ndarray, aa: np.ndarray, bb: np.ndarray) -> np.ndarray:
    """Evaluate the Genz continuous function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values increase
        the rate of exponential decay and make integration more challenging.
    bb : np.ndarray
        An array of offset parameters of length ``M``; minimal effect on
        integration difficulty.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.exp(-1 * np.sum(np.abs(xx - bb) * aa, axis=1))

    return yy


def corner_peak(xx: np.ndarray, aa: np.ndarray) -> np.ndarray:
    """Evaluate the Genz corner peak function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values increase
        the prominence of the peak and make integration more challenging.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    dim = xx.shape[1]

    yy = (1 + (xx @ aa)) ** (-(dim + 1))

    return yy


def discontinuous(
    xx: np.ndarray,
    aa: np.ndarray,
    bb: np.ndarray,
) -> np.ndarray:
    """Evaluate the Genz discontinuous function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values increase
        the rate of exponential rise and make integration more challenging.
    bb : np.ndarray
        An array of offset parameters of length ``M``; define the boundary
        of the non-zero region — larger values expand the non-zero region
        and increase the integral.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.exp(np.sum(xx * aa, axis=1))

    # Filter the output to make the function discontinuous
    mask = np.zeros(xx.shape[0], dtype=bool)
    for i in range(xx.shape[1]):
        mask |= xx[:, i] > bb[i]
    yy[mask] = 0

    return yy


def gaussian(xx: np.ndarray, aa: np.ndarray, bb: np.ndarray) -> np.ndarray:
    """Evaluate the Genz Gaussian function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values produce
        a narrower peak and make integration more challenging.
    bb : np.ndarray
        An array of offset parameters of length ``M``; define the location
        of the peak center.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.exp(-1 * np.sum((xx - bb) ** 2 * aa**2, axis=1))

    return yy


def oscillatory(xx: np.ndarray, aa: np.ndarray, b: float) -> np.ndarray:
    """Evaluate the Genz oscillatory function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values increase
        the oscillation frequency and make integration more challenging.
    b : float
        Scalar offset parameter; minimal effect on integration difficulty.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.cos(2 * np.pi * b + np.sum(xx * aa, axis=1))

    return yy


def product_peak(
    xx: np.ndarray,
    aa: np.ndarray,
    bb: np.ndarray,
) -> np.ndarray:
    """Evaluate the Genz product peak function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, M)`` array of input values where ``N`` is the number of
        evaluation points and ``M`` is the input dimension.
    aa : np.ndarray
        An array of shape parameters of length ``M``; larger values increase
        the prominence of the peak and make integration more challenging.
    bb : np.ndarray
        An array of offset parameters of length ``M``; define the location
        of the peak center.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
    """
    yy = np.prod(1 / ((xx - bb) ** 2 + aa ** (-2)), axis=1)

    return yy
