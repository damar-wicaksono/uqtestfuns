"""
Module with routines involving the truncated normal probability distribution.

The truncated normal distribution in UQTestFuns is parameterized by four
parameters: ``mu``, ``sigma``, ``lb``, and ``ub`` that correspond to
the mean, the standard deviation, lower bound, and upper bound, respectively.

The underlying implementation is based on the implementation of scipy.stats.
In the SciPy implementation, the truncated normal is parameterized also by
four parameters but with different meaning: a, b, loc, and scale. loc and scale
correspond to the mu and sigma of the underlying normal distribution, while
a and b correspond to the lower and upper bound, respectively.
However, the lower and upper bounds correspond to the standard normal
distribution.

One might think that, for instance, with loc = 0.5 and scale = 0.1,
and a = 0 and b = 1, the distribution will be centered on 0.5
and cut at 0 and 1.
Yet, this is not what the scipy.stats.beta does.
Instead, it is a truncated standard normal at 0 and 1 then shift to the new
``loc`` of 0.5; the lower and upper bounds are actually, 0.5 and 1.5,
respectively.

The translation between parameterization of the distribution in UQTestFuns
and SciPy is as follows:

- ``a`` = ``(lb - mu) / sigma``
- ``b`` = ``(ub - mu) / sigma``
- ``loc`` = ``mu``
- ``scale`` = ``sigma``

where lb and ub are the desired lower and upper bounds of the truncated
normal distribution, respectively.
"""

import numpy as np

from scipy.stats import truncnorm
from typing import Tuple

from . import normal
from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "trunc-normal"

NUM_PARAMS = 4


def _get_parameters(
    parameters: ARRAY_FLOAT,
) -> Tuple[float, float, float, float]:
    """Get the parameters of a truncated normal dist. w/ intuitive names.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated normal distribution.

    Returns
    -------
    Tuple[float, float, float, float]
        The mean, standard deviation, lower bound, and upper bound of the
        truncated normal distribution.
    """
    mu = float(parameters[0])
    sigma = float(parameters[1])
    lb = float(parameters[2])
    ub = float(parameters[3])

    return mu, sigma, lb, ub


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a truncated normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated normal distribution
        (i.e., the mean, standard deviation, and the lower and upper bounds).

    Returns
    ------
    None
        The function exits without any return value if nothing is wrong.

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    # Verify overall shape
    verify_param_nums(parameters.size, NUM_PARAMS, DISTRIBUTION_NAME)

    mu, sigma, lb, ub = _get_parameters(parameters)

    # Check validity of values
    if sigma <= 0.0:
        raise ValueError(
            f"The standard deviation {sigma} "
            f"must be larger than 0.0 (positive)!"
        )

    if lb >= ub:
        raise ValueError(
            f"The lower bound {lb} "
            f"cannot be equal or greater than the upper bound {ub}!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a truncated normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated normal distribution.

    Returns
    -------
    float
        The lower bound of the truncated normal distribution.
    """
    _, _, lower_bound, _ = _get_parameters(parameters)

    # Get the lower bound of the normal distribution
    lb_normal = normal.lower(parameters[:2])
    if lower_bound < lb_normal:
        # Use the corresponding normal lower bound instead
        return lb_normal

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a truncated normal distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated normal distribution

    Returns
    -------
    float
        The upper bound of the truncated normal distribution.
    """
    _, _, _, upper_bound = _get_parameters(parameters)

    # Get the upper bound of the normal distribution
    ub_normal = normal.upper(parameters[:2])
    if upper_bound > ub_normal:
        # Use the corresponding normal upper bound instead
        return ub_normal

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a truncated normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a truncated normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the truncated normal distribution.
    lower_bound : float
        Lower bound of the truncated normal distribution.
    upper_bound : float
        Upper bound of the truncated normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        PDF values of the truncated normal distribution on the sample values.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    - ``lower_bound`` and ``upper_bound`` in the function parameters may not
      be the same as the ones in ``parameters`` as the former are already
      processed setting the numerical bounds when the given bounds are outside
      them.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    # NOTE: Don't use the original bounds as "lower_bound" and "upper_bound"
    # may have been further truncated for numerical reason.
    mu, sigma, _, _ = _get_parameters(parameters)

    yy[idx] = truncnorm.pdf(
        xx[idx],
        a=(lower_bound - mu) / sigma,
        b=(upper_bound - mu) / sigma,
        loc=mu,
        scale=sigma,
    )

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of the truncated normal distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a truncated normal distribution.
    parameters : ARRAY_FLOAT
        Parameters of the truncated normal distribution.
    lower_bound : float
        Lower bound of the truncated normal distribution.
    upper_bound : float
        Upper bound of the truncated normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the truncated normal distribution on the sample values.

    Notes
    -----
    - CDF for sample with values smaller (resp. larger) than the lower bound
      (resp. upper bound) are set to 0.0 (resp. 1.0).
    - ``lower_bound`` and ``upper_bound`` in the function parameters may not
      be the same as the ones in ``parameters`` as the former are already
      processed setting the numerical bounds when the given bounds are outside
      them.
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    # NOTE: Don't use the original bounds as "lower_bound" and "upper_bound"
    # may have been further truncated for numerical reason.
    mu, sigma, _, _ = _get_parameters(parameters)

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = truncnorm.cdf(
        xx[idx_rest],
        a=(lower_bound - mu) / sigma,
        b=(upper_bound - mu) / sigma,
        loc=mu,
        scale=sigma,
    )

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a truncated normal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of a truncated normal distribution.
    lower_bound : float
        Lower bound of the truncated normal distribution.
    upper_bound : float
        Upper bound of the truncated normal distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the truncated normal distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN according to
      the underlying SciPy implementation.
    - ``lower_bound`` and ``upper_bound`` in the function parameters may not
      be the same as the ones in ``parameters`` as the former are already
      processed setting the numerical bounds when the given bounds are outside
      them.
    """
    # NOTE: Don't use the original bounds as "lower_bound" and "upper_bound"
    # may have been further truncated for numerical reason.
    mu, sigma, _, _ = _get_parameters(parameters)

    # Compute the ICDF
    yy = truncnorm.ppf(
        xx,
        a=(lower_bound - mu) / sigma,
        b=(upper_bound - mu) / sigma,
        loc=mu,
        scale=sigma,
    )

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
