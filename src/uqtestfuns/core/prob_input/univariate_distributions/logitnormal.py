"""
Module with routines involving the logit-normal probability distribution.

A logit-normal random variable is a random variable whose logit transformation
is a normal random variable.

The logit-normal distribution in UQTestFuns is parametrized by two parameters:
mu and sigma, the mean and standard deviation of the underlying normal
distribution, respectively.

The underlying implementation is based on the implementation from scipy.stats.
In the SciPy implementation, the mean (mu) corresponds
to the ``loc`` parameter, while the standard deviation (sigma) corresponds
to the ``scale`` parameter.
"""

import numpy as np
from scipy.stats import norm
from scipy.special import logit
from scipy.special import expit as logistic

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "logitnormal"

NUM_PARAMS = 2


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a logit-normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a logit-normal distribution
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
    """Get the lower bound of a logit-normal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a logit-normal distribution (not used).

    Returns
    -------
    float
        The lower bound of the logit-normal distribution.

    Notes
    -----
    - A logit-normal distribution is bounded on the left at 0.0.
    - The parameters of the logit-normal distribution is part of the function
      parameterization for interface consistency.
    """
    lower_bound = 0.0

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a logit-normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a logit-normal distribution

    Returns
    -------
    float
        The upper bound of the logit-normal distribution.

    Notes
    -----
    - A logit-normal distribution is bounded on the left at 1.0.
    - The parameters of the logit-normal distribution is part of the function
      parameterization for interface consistency.
    """
    upper_bound = 1.0

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a logit-normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a logit-normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the logit-normal distribution.
    lower_bound : float
        Lower bound of the logit-normal distribution.
    upper_bound : float
        Upper bound of the logit-normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        PDF values of the logit-normal distribution on the sample values.

    Notes
    -----
    - The PDF for sample with values outside the bounds are set to 0.0.
    """
    xx_trans = logit(xx)
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx > 0.0, xx < 1.0)
    yy[idx] = (
        norm.pdf(xx_trans[idx], loc=parameters[0], scale=parameters[1])
        / xx[idx]
        / (1 - xx[idx])
    )

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a logit-normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a logit-normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the logit-normal distribution.
    lower_bound : float
        Lower bound of the logit-normal distribution.
    upper_bound : float
        Upper bound of the logit-normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the logit-normal distribution on the sample values.

    Notes
    -----
    - The CDF for sample with values smaller (resp. larger)
      than the lower bound (resp. upper bound) are set to 0.0 (resp. 1.0).
    """
    xx_trans = logit(xx)
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = norm.cdf(
        xx_trans[idx_rest], loc=parameters[0], scale=parameters[1]
    )

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a logit-normal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of a logit-normal distribution.
    lower_bound : np.ndarray
        Lower bound of the logit-normal distribution.
    upper_bound : np.ndarray
        Upper bound of the logit-normal distribution.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the logit-normal distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN according to
      the underlying SciPy implementation.
    """

    # Compute the ICDF
    yy = logistic(norm.ppf(xx, loc=parameters[0], scale=parameters[1]))

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
