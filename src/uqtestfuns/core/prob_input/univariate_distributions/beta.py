"""
Module with routines involving the Beta probability distribution.

The Beta distribution in UQTestFuns is parameterized by four parameters:
``r``, ``s``, ``a``, and ``b``. ``r`` and ``s`` are the shape parameters,
while ``a`` and ``b`` are the lower and upper bounds, respectively.

The underlying implementation is based on the implementation of scipy.stats.
In the SciPy implementation, the Beta distribution is parameterized also
by four parameters: ``a``, ``b``, ``loc``, and ``scale``.
``a`` and ``b`` are the shape parameters, while ``loc`` and ``scale`` are
the shifting and scaling parameters, respectively.

The translation between parameterization of the distribution in UQTestFuns
and SciPy is as follows:

- ``a`` == ``r``
- ``b`` == ``s``
- ``loc`` == ``a``
- ``scale`` == ``(b-a)``
"""

import numpy as np

from scipy.stats import beta

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT


DISTRIBUTION_NAME = "beta"

NUM_PARAMS = 4


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a Beta distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a Beta distribution
        (i.e., the two shape parameters and the lower and upper bounds).

    Returns
    ------
    None
        Function exits without any return value when nothing is wrong.

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    # Check overall shape
    verify_param_nums(parameters.size, NUM_PARAMS, DISTRIBUTION_NAME)

    # Check validity of values
    if parameters[0] <= 0.0 or parameters[1] <= 0.0:
        raise ValueError(
            f"The shape parameters {parameters[0]} and {parameters[1]}"
            f"must be larger than 0.0 (positive)!"
        )

    if parameters[2] >= parameters[3]:
        raise ValueError(
            f"The lower bound {parameters[2]} "
            f"cannot be equal or greater than the upper bound {parameters[3]}!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a Beta distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a Beta distribution.

    Returns
    -------
    float
        The lower bound of the Beta distribution.
    """
    lower_bound = float(parameters[2])

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a Beta distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a Beta distribution

    Returns
    -------
    float
        The upper bound of the Beta distribution.
    """
    upper_bound = float(parameters[3])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a Beta distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a Beta distribution.
    parameters : ARRAY_FLOAT
        Parameters of the Beta distribution.
    lower_bound : float
        Lower bound of the Beta distribution.
    upper_bound : float
        Upper bound of the Beta distribution.

    Returns
    -------
    ARRAY_FLOAT
        PDF values of the Beta distribution on the sample values.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)
    yy[idx] = beta.pdf(
        xx[idx],
        a=parameters[0],
        b=parameters[1],
        loc=parameters[2],
        scale=parameters[3] - parameters[2],
    )

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of the Beta distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a Beta distribution.
    parameters : ARRAY_FLOAT
        Parameters of the Beta distribution.
    lower_bound : float
        Lower bound of the Beta distribution.
    upper_bound : float
        Upper bound of the Beta distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the Beta distribution on the sample values.

    Notes
    -----
    - CDF for sample with values smaller (resp. larger) than the lower bound
      (resp. upper bound) are set to 0.0 (resp. 1.0).
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = beta.cdf(
        xx[idx_rest],
        a=parameters[0],
        b=parameters[1],
        loc=parameters[2],
        scale=parameters[3] - parameters[2],
    )

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a Beta distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) in the [0, 1] domain.
    parameters : ARRAY_FLOAT
        Parameters of a Beta distribution.
    lower_bound : float
        Lower bound of the Beta distribution.
    upper_bound : float
        Upper bound of the Beta distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the Beta distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN according to
      the underlying SciPy implementation.
    """
    # Get the parameters
    r, s, a, b = parameters[:]

    # Compute the ICDF
    yy = beta.ppf(xx, a=r, b=s, loc=a, scale=b - a)

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
