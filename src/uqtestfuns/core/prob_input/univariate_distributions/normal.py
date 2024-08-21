"""
Module with routines involving the normal (Gaussian) probability distribution.

The normal distribution in UQTestFuns is parametrized by two parameters:
mu and sigma, the mean and standard deviation, respectively.

The underlying implementation is based on the implementation from scipy.stats.
In the SciPy convention, the mean (mu) corresponds to the ``loc`` parameter,
while the standard deviation (sigma) corresponds to the ``scale`` parameter.
"""

import numpy as np
from scipy.stats import norm

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "normal"

NUM_PARAMS = 2


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a normal distribution
        (i.e., the mean and standard deviation).

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

    if parameters[1] <= 0.0:
        raise ValueError(
            f"The corresponding standard deviation {parameters[1]}"
            f"must be larger than 0.0!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a normal distribution.

    Returns
    -------
    float
        The lower bound of the normal distribution.

    Notes
    -----
    - Strictly speaking, a normal distribution is unbounded on the left.
      However, for numerical reason a lower bound is set.
    - The lower bound of the normal distribution is chosen such that
      the probability mass between the lower and upper bound is at least
      1 - 1e-15.
    """
    # -8.222082216130435 is the quantile values with probability of 1e-16
    # for the standard Normal distribution (mu = 0.0, sigma = 1.0)
    lower_bound = float(-8.222082216130435 * parameters[1] + parameters[0])

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a normal distribution

    Returns
    -------
    float
        The upper bound of the normal distribution.

    Notes
    -----
    - Strictly speaking, a normal distribution is unbounded on the right.
      However, for numerical reason an upper bound is set.
    - The upper bound of the normal distribution is chosen such that
      tbe probability mass between the lower and upper bound is at least
      1 - 1e-15.
    """
    # 8.209536151601387 is the quantile values with probability of 1-1e-16
    # for the standard Normal distribution (mu = 0.0, sigma = 1.0)
    upper_bound = float(8.209536151601387 * parameters[1] + parameters[0])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the normal distribution.
    lower_bound : float
        Lower bound of the normal distribution.
    upper_bound : float
        Upper bound of the normal distribution.

    Returns
    -------
    np.ndarray
        PDF values of the normal distribution on the sample values.

    Notes
    -----
    - The PDF for sample with values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)
    yy[idx] = norm.pdf(xx[idx], loc=parameters[0], scale=parameters[1])

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the normal distribution.
    lower_bound : float
        Lower bound of the normal distribution.
    upper_bound : float
        Upper bound of the normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the normal distribution on the sample values.

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
    yy[idx_rest] = norm.cdf(
        xx[idx_rest], loc=parameters[0], scale=parameters[1]
    )

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of a normal distribution.
    lower_bound : float
        Lower bound of the normal distribution.
    upper_bound : float
        Upper bound of the normal distribution.

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
    yy = norm.ppf(xx, loc=parameters[0], scale=parameters[1])

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
