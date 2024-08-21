"""
Module with routines involving the truncated Gumbel (max.) probability dist.

The truncated Gumbel (max.) distribution in UQTestFuns is parameterized by
four parameters: ``mu``, ``beta``, ``lb``, and ``ub`` that correspond to
the mode, the scale, lower bound, and upper bound, respectively.

The underlying implementation is based on the re-implementation of regular
Gumbel (max.) distribution in UQTestFuns (which in turn, based on scipy.stats).
"""

import numpy as np

from scipy.stats import gumbel_r
from typing import Tuple

from . import gumbel
from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "trunc-gumbel"

NUM_PARAMS = 4


def _get_parameters(
    parameters: ARRAY_FLOAT,
) -> Tuple[float, float, float, float]:
    """Get the parameters of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated Gumbel (max.) distribution.

    Returns
    -------
    Tuple[float, float, float, float]
        The mode (mu), scale (beta) lower bound, and upper bound
        of the truncated Gumbel (max.) distribution
        (in that order, as a tuple).
    """
    mu = float(parameters[0])
    beta = float(parameters[1])
    lb = float(parameters[2])
    ub = float(parameters[3])

    return mu, beta, lb, ub


def _compute_normalizing_factor(
    mu: float,
    beta: float,
    lb: float,
    ub: float,
) -> float:
    """Compute the normalizing factor of the truncated distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated Gumbel (max.) distribution.

    Returns
    -------
    float
        The normalizing factor for the truncated distribution.
    """

    lb_quantile = gumbel_r.cdf(lb, loc=mu, scale=beta)
    ub_quantile = gumbel_r.cdf(ub, loc=mu, scale=beta)

    normalizing_factor = ub_quantile - lb_quantile

    return normalizing_factor


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated Gumbel (max.) distribution
        (i.e., mu, beta, lower bound, and upper bound).

    Returns
    -------
    None
        The function exits without any return value when nothing is wrong.

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shape is inconsistent.
    """
    # Verify overall shape
    verify_param_nums(parameters.size, NUM_PARAMS, DISTRIBUTION_NAME)

    mu, beta, lb, ub = _get_parameters(parameters)

    # Verify the first two parameters
    gumbel.verify_parameters(parameters[:2])

    # Check the validity of the parameter values w.r.t the bounds
    if lb >= ub:
        raise ValueError(
            f"The lower bound of a truncated Gumbel (max.) distribution {lb} "
            f"cannot be equal or greater than the upper bound {ub}!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated Gumbel (max.) distribution.

    Returns
    -------
    float
        The lower bound of the truncated Gumbel (max.) distribution.
    """
    _, _, lower_bound, _ = _get_parameters(parameters)

    # Get the upper bound of the untruncated Gumbel distribution
    lb_gumbel = gumbel.lower(parameters[:2])
    if lower_bound < lb_gumbel:
        # Use the corresponding normal lower bound instead
        return lb_gumbel

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a truncated Gumbel (max.) distribution.

    Returns
    -------
    float
        The upper bound of the truncated Gumbel (max.) distribution.
    """
    _, _, _, upper_bound = _get_parameters(parameters)

    # Get the upper bound of the untruncated Gumbel distribution
    ub_gumbel = gumbel.upper(parameters[:2])
    if upper_bound > ub_gumbel:
        # Use the corresponding Gumbel upper bound instead
        return ub_gumbel

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a truncated Gumbel (max.) distribution.
    parameters : ARRAY_FLOAT
        Parameters of the truncated Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of the truncated Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of the truncated Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        PDF values of the truncated Gumbel (max.) distribution
        on the sample values.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    - ``lower_bound`` and ``upper_bound`` in the function parameters are the
      same as the ones in ``parameters``. For a truncated Gumbel (max.)
      distribution, the bounds are part of the parameterization.
    """
    # Get the parameters
    mu, beta, _, _ = _get_parameters(parameters)

    # Get the non-zero indices (within the bounds)
    idx_non_zero = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    # Compute the normalizing factor
    normalizing_factor = _compute_normalizing_factor(
        mu, beta, lower_bound, upper_bound
    )

    # Compute the PDF
    yy = np.zeros(xx.shape)
    yy[idx_non_zero] = gumbel_r.pdf(xx[idx_non_zero], loc=mu, scale=beta)
    yy[idx_non_zero] = yy[idx_non_zero] / normalizing_factor

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of the truncated Gumbel (max.) distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a truncated Gumbel (max.) distribution.
    parameters : ARRAY_FLOAT
        Parameters of the truncated Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of the truncated Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of the truncated Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the truncated Gumbel (max.) distribution
        on the sample values.

    Notes
    -----
    - CDF for sample with values smaller (resp. larger) than the lower bound
      (resp. upper bound) are set to 0.0 (resp. 1.0).
    - ``lower_bound`` and ``upper_bound`` in the function parameters are the
      same as the ones in ``parameters``. For a truncated Gumbel (max.)
      distribution, the bounds are part of the parameterization.
    """
    # Get the parameters
    mu, beta, _, _ = _get_parameters(parameters)

    # Get the relevant indices
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    # Compute the normalizing factor
    normalizing_factor = _compute_normalizing_factor(
        mu, beta, lower_bound, upper_bound
    )

    # Compute the CDF
    yy = np.empty(xx.shape)
    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = gumbel_r.cdf(xx[idx_rest], loc=mu, scale=beta)
    yy[idx_rest] = yy[idx_rest] - gumbel_r.cdf(lower_bound, loc=mu, scale=beta)
    yy[idx_rest] = yy[idx_rest] / normalizing_factor

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a truncated Gumbel (max.) distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of a truncated Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of the truncated Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of the truncated Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the truncated Gumbel (max.)
        distribution.

    Notes
    -----
    - ICDF for sample with values of 0.0 and 1.0 are automatically set to the
      lower bound and upper bound, respectively.
    - ``lower_bound`` and ``upper_bound`` in the function parameters may not
      be the same as the ones in ``parameters``. If one of the bounds is
      initially set to inf, then it would be automatically set to the bounds
      of the regular Gumbel.
    TODO: values outside [0, 1] must either be an error or NaN
    """

    # Get the parameters
    mu, beta, _, _ = _get_parameters(parameters)

    # Compute the normalizing factor
    # NOTE: Use the processed bounds
    normalizing_factor = _compute_normalizing_factor(
        mu, beta, lower_bound, upper_bound
    )

    # Make sure values outside [0.0, 1.0] are set to NaN
    xx[xx < 0.0] = np.nan
    xx[xx > 1.0] = np.nan

    # Compute the ICDF
    cdf_values = (
        gumbel_r.cdf(lower_bound, loc=mu, scale=beta) + normalizing_factor * xx
    )
    yy = gumbel.icdf(cdf_values, parameters[:2], lower_bound, upper_bound)

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
