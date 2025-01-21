"""
Module with routines involving the uniform probability distribution.

The uniform distribution in UQTestFuns is parametrized by two parameters:
the lower and upper bounds.
"""

import numpy as np

from .utils import postprocess_icdf, verify_param_nums
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "uniform"

NUM_PARAMS = 2


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of the uniform distribution
        (i.e., lower and upper bounds).

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

    if parameters[0] >= parameters[1]:
        raise ValueError(
            f"The lower bound {parameters[0]} "
            f"cannot be greater than the upper bound {parameters[1]}!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a uniform distribution.

    Returns
    -------
    float
        The lower bound of the uniform distribution.
    """
    lower_bound = float(parameters[0])

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a uniform distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a uniform distribution.

    Returns
    -------
    float
        The upper bound of the uniform distribution.
    """
    upper_bound = float(parameters[1])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a uniform distribution.
    parameters : ARRAY_FLOAT
        Parameters of the uniform distribution.
    lower_bound: float
        Lower bound of the uniform distribution.
    upper_bound: float
        Upper bound of the distribution.

    Returns
    -------
    ARRAY_FLOAT
        The PDF values of the uniform distribution.

    Notes
    -----
    - The sample values ``xx`` themselves are not used in the computation of
      density value (it is, after all, a constant),
      but required nevertheless as the function is vectorized.
      Given a vector input, the function should return the PDF values of the
      same length as the input.
      Moreover, this signature must be consistent with the other distributions.
    - The values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    yy[idx] = 1 / (np.diff(parameters))

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a uniform distribution.
    parameters : ARRAY_FLOAT
        Parameters of the uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution
    upper_bound : float
        Upper bound of the uniform distribution.

    Returns
    -------
    ARRAY_FLOAT
        The CDF values of the uniform distribution.

    Notes
    -----
    - The CDF values for sample values below the lower bound are set to 0.0,
      and for sample values above the upper bound are set to 1.0.
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = (xx[idx_rest] - parameters[0]) / np.diff(parameters)

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a uniform distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of a uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution.
    upper_bound : float
        Upper bound of the uniform distribution.
        This parameter is not used but must appear for interface consistency.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the uniform distribution.
    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN.
    """
    xx[xx < 0.0] = np.nan
    xx[xx > 1.0] = np.nan

    # Compute the ICDF
    yy = (lower_bound + np.diff(parameters) * xx).astype(np.float64)

    # Check if values are within the set bounds
    yy_post = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy_post
