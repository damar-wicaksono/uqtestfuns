"""
Module with routines involving the lognormal probability distribution.

The lognormal distribution in UQTestFuns is parameterized by two parameters:
``lambda`` and ``xi``, the mean and standard deviation of the underlying normal
distribution, respectively.

The underlying implementation is based on the implementation of scipy.stats.
In the SciPy implementation, the lognormal distribution is parameterized by
two parameters: ``s`` and ``scale``, the shape and scaling parameters,
respectively. The shape parameter ``s`` corresponds to the standard deviation
of the underlying normal distribution.

The translation between parameterization of the distribution in UQTestFuns
and SciPy is as follows:

- ``s`` = ``xi``
- ``scale`` = ``np.exp(lambda)``
"""
import numpy as np
from scipy.stats import lognorm

from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "lognormal"


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a lognormal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the lognormal distribution
        (i.e., the mean and standard deviation of the associated normal
        distribution).

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
    if parameters.size != 2:
        raise ValueError(
            f"A lognormal distribution requires two parameters!"
            f"Expected 2, got {parameters.size}."
        )

    if parameters[1] <= 0.0:
        raise ValueError(
            f"The corresponding normal standard deviation {parameters[1]}"
            f"must be larger than 0.0!"
        )


def lower(parameters: ARRAY_FLOAT) -> float:
    """Get the lower bound of a lognormal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a lognormal distribution.

    Returns
    -------
    float
        The lower bound of the lognormal distribution.

    Notes
    -----
    - The parameters are not used in determining the lower bound of
      the distribution; it must, however, appear for interface consistency.
      The lower bound of a lognormal distribution is finite; it is 0.0.
    """
    lower_bound = 0.0

    return lower_bound


def upper(parameters: ARRAY_FLOAT) -> float:
    """Get the upper bound of a lognormal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a lognormal distribution.

    Returns
    -------
    float
        The upper bound of the lognormal distribution.

    Notes
    -----
    - Strictly speaking, a lognormal distribution is unbounded on the right.
      However, for numerical reason an upper bound is set.
    - The upper bound of the lognormal distribution is chosen such that
      the probability mass between 0.0 (the lower bound) and the upper bound
      is at least 1 - 1e-15.
    """
    # 8.209536151601387 is the quantile values with probability of 1-1e-16
    # for the corresponding standard Normal dist. (mu = 0.0, beta = 1.0)
    upper_bound = float(
        np.exp(8.209536151601387 * parameters[1] + parameters[0])
    )

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a lognormal distribution.
    parameters : np.ndarray
        Parameters of the lognormal distribution.
    lower_bound : float
        Lower bound of the lognormal distribution.
    upper_bound : float
        Upper bound of the lognormal distribution.

    Returns
    -------
    np.ndarray
        PDF values of the lognormal distribution on the sample values.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)
    yy[idx] = lognorm.pdf(
        xx[idx], s=parameters[1], scale=np.exp(parameters[0])
    )

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a lognormal distribution.
    parameters : np.ndarray
        Parameters of the lognormal distribution.
    lower_bound : float
        Lower bound of the lognormal distribution.
    upper_bound : float
        Upper bound of the lognormal distribution.

    Returns
    -------
    np.ndarray
        CDF values of the lognormal distribution on the sample values.

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
    yy[idx_rest] = lognorm.cdf(
        xx[idx_rest], s=parameters[1], scale=np.exp(parameters[0])
    )

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of a lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of a lognormal distribution.
    lower_bound : float
        Lower bound of the lognormal distribution.
    upper_bound : float
        Upper bound of the lognormal distribution.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the lognormal distribution.

    Notes
    -----
    - ICDF for sample with values of 0.0 and 1.0 are automatically set to the
      lower bound and upper bound, respectively.
    """
    yy = np.zeros(xx.shape)
    idx_lower = xx == 0.0
    idx_upper = xx == 1.0
    idx_rest = np.logical_not(idx_upper)

    yy[idx_lower] = lower_bound
    yy[idx_upper] = upper_bound
    yy[idx_rest] = lognorm.ppf(
        xx[idx_rest], s=parameters[1], scale=np.exp(parameters[0])
    )

    return yy
