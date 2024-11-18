"""
Module with routines involving the exponential probability distribution.

The exponential distribution in UQTestFuns is parametrized by a single
parameter: the rate parametere.

The underlying implementation is based on the implementation from scipy.stats.
In the SciPy convention, the rate parameter corresponds to the reciprocal
of the ``scale`` parameter.
"""

import numpy as np
from scipy.stats import expon

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "exponential"

NUM_PARAMS = 1


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of an exponential distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameter of an exponential distribution
        (i.e., the rate parameter).

    Returns
    ------
    None
        The function exits without any return value when nothing is wrong.

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    # Verify overall shape
    verify_param_nums(parameters.size, NUM_PARAMS, DISTRIBUTION_NAME)

    if parameters[0] <= 0.0:
        raise ValueError(
            f"The corresponding rate parameter {parameters[0]}"
            f"must be larger than 0.0!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of an exponential distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameter of an exponential distribution.

    Returns
    -------
    float
        The lower bound of the exponential distribution.

    Notes
    -----
    - The parameters are not used in determining the lower bound of
      the distribution; it must, however, appear for interface consistency.
      The lower bound of a lognormal distribution is finite; it is 0.0.
    """
    lower_bound = 0.0

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of an exponential distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of an exponential distribution

    Returns
    -------
    float
        The upper bound of the exponential distribution.

    Notes
    -----
    - Strictly speaking, an exponential distribution is unbounded on the right.
      However, for numerical reason an upper bound is set.
    - The upper bound of the exponential distribution is chosen such that
      tbe probability mass between the lower and upper bound is at least
      1 - 1e-15.
    """
    # 36.7368005696771 is the quantile values with probability of 1-1e-16
    # for the exponential distribution with rate parameter value 1.0
    upper_bound = float(36.7368005696771 / parameters[0])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of an exponential distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of an exponential distribution.
    parameters : ARRAY_FLOAT
        Parameters of the exponential distribution.
    lower_bound : float
        Lower bound of the exponential distribution.
    upper_bound : float
        Upper bound of the exponential distribution.

    Returns
    -------
    np.ndarray
        PDF values of the exponential distribution on the sample values.

    Notes
    -----
    - The PDF for sample with values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)
    rate = parameters[0]
    scale = 1 / rate
    yy[idx] = expon.pdf(xx[idx], scale=scale)

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of an exponential distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of an exponential distribution.
    parameters : ARRAY_FLOAT
        Parameters of the exponential distribution.
    lower_bound : float
        Lower bound of the exponential distribution.
    upper_bound : float
        Upper bound of the exponential distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the exponential distribution on the sample values.

    Notes
    -----
    - The CDF for sample with values smaller (resp. larger)
      than the lower bound (resp. upper bound) are set to 0.0 (resp. 1.0).
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    rate = parameters[0]
    scale = 1 / rate
    yy[idx_rest] = expon.cdf(xx[idx_rest], scale=scale)

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of an exponential distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of an exponential distribution.
    lower_bound : float
        Lower bound of the exponential distribution.
    upper_bound : float
        Upper bound of the exponential distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the normal distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN according to
      the underlying SciPy implementation.
    """

    # Compute the ICDF
    rate = parameters[0]
    scale = 1 / rate
    yy = expon.ppf(xx, scale=scale)

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
