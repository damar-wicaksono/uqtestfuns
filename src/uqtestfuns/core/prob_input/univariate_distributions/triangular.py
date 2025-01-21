"""
Module with routines involving the Triangular probability distribution.

The Triangular distribution in UQTestFuns is parameterized
by three parameters: a, b, and c.
These are the lower bound, upper bound, and the mid-point (i.e., modal value),
respectively.

The density value at the modal value is computed such that the area under
the distribution is 1.0.
"""

import numpy as np

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "triangular"

NUM_PARAMS = 3


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a triangular distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a triangular distribution (i.e., the lower bound,
        upper bound, and modal value).

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

    if not (parameters[0] < parameters[2] < parameters[1]):
        raise ValueError(
            f"The parameters must be: lower bound {parameters[0]} "
            f"< upper bound {parameters[1]} "
            f"< modal value {parameters[2]}."
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a triangular distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a triangular distribution.

    Returns
    -------
    float
        The lower bound of the triangular distribution.
    """
    lower_bound = float(parameters[0])

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a triangular distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a triangular distribution.

    Returns
    -------
    float
        The upper bound of a triangular distribution.
    """
    upper_bound = float(parameters[1])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a triangular distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a triangular distribution.
    parameters : ARRAY_FLOAT
        Parameters of the triangular distribution.
    lower_bound : float
        Lower bound of the triangular distribution.
    upper_bound : float
        Upper bound of the triangular distribution.

    Returns
    -------
    ARRAY_FLOAT
        The PDF values of the triangular distribution.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    """
    mid_point = parameters[2]
    yy = np.zeros(xx.shape)
    idx_below_mid = np.logical_and(xx >= lower_bound, xx <= mid_point)
    idx_above_mid = np.logical_and(xx > mid_point, xx <= upper_bound)

    modal_density = 2 / (upper_bound - lower_bound)
    yy[idx_below_mid] = (
        modal_density
        / (mid_point - lower_bound)
        * (xx[idx_below_mid] - lower_bound)
    )
    yy[idx_above_mid] = (
        modal_density
        / (upper_bound - mid_point)
        * (upper_bound - xx[idx_above_mid])
    )

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a triangular distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a triangular distribution.
    parameters : ARRAY_FLOAT
        Parameters of the triangular distribution.
    lower_bound : float
        Lower bound of the triangular distribution.
    upper_bound : float
        Upper bound of the triangular distribution.

    Returns
    -------
    ARRAY_FLOAT
        The CDF values of the triangular distribution.

    Notes
    -----
    - The CDF values for sample values below the lower bound are set to 0.0,
      and for sample values above the upper bound are set to 1.0.
    """

    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    mid_point = parameters[2]
    idx_below_mid = np.logical_and(xx >= lower_bound, xx <= mid_point)
    idx_above_mid = np.logical_and(xx > mid_point, xx <= upper_bound)

    yy = np.empty(xx.shape)
    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_below_mid] = (
        (xx[idx_below_mid] - lower_bound) ** 2
        / (upper_bound - lower_bound)
        / (mid_point - lower_bound)
    )
    yy[idx_above_mid] = 1 - (upper_bound - xx[idx_above_mid]) ** 2 / (
        upper_bound - lower_bound
    ) / (upper_bound - mid_point)

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a triangular distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT:
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of the triangular distribution.
    lower_bound : float
        Lower bound of the triangular distribution.
    upper_bound : float
        Upper bound of the triangular distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the triangular distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN.
    """
    mid_point = parameters[2]
    mid_point_quantile = (mid_point - lower_bound) / (
        (upper_bound - lower_bound)
    )
    idx_below_mid = np.logical_and(xx >= 0.0, xx <= mid_point_quantile)
    idx_above_mid = np.logical_and(xx > mid_point_quantile, xx <= 1.0)
    idx_nan = np.logical_not(np.logical_or(idx_below_mid, idx_above_mid))

    yy = np.empty(xx.shape)
    yy[idx_below_mid] = lower_bound + np.sqrt(
        xx[idx_below_mid]
        * (upper_bound - lower_bound)
        * (mid_point - lower_bound)
    )

    yy[idx_above_mid] = upper_bound - np.sqrt(
        (1 - xx[idx_above_mid])
        * (upper_bound - lower_bound)
        * (upper_bound - mid_point)
    )

    yy[idx_nan] = np.nan

    # Check if values are within the set bounds
    yy_post = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy_post
