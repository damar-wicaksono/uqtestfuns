"""
Module with routines involving the Gumbel maximum probability distribution.

The Gumbel distribution in UQTestFuns is parameterized by two parameters:
``mu`` and ``beta``.

The underlying implementation is based on the implementation from scipy.stats
(specifically, ``gumbel_r``  the right-skewed Gumbel).
In the SciPy convention, the parameter ``mu`` corresponds
to the ``loc`` parameter, while the parameter ``beta``
corresponds to the ``scale`` parameter.
"""

import numpy as np

from scipy.stats import gumbel_r

from .utils import verify_param_nums, postprocess_icdf
from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "gumbel"

NUM_PARAMS = 2


def verify_parameters(parameters: ARRAY_FLOAT) -> None:
    """Verify the parameters of a Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a Gumbel (max.) distribution
        (i.e., the mu and beta parameters).

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
            f"The corresponding beta parameter {parameters[1]} "
            f"of a {DISTRIBUTION_NAME} must be larger than 0.0!"
        )


def lower(parameters: ARRAY_FLOAT):
    """Get the lower bound of a Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a Gumbel (max.) distribution.

    Returns
    -------
    float
        The lower bound of the Gumbel (max.) distribution.

    Notes
    -----
    - Strictly speaking, a Gumbel (max.) distribution is unbounded on both
      sides. However, for numerical reason a lower bound is set.
    - The probability mass contained up to the lower bound of the Gumbel (max.)
      distribution is at most 1e-15.
    - The difference between 1.0 and the probability mass between lower and
      upper bounds is at most 1e-15.
    """
    # 3.606621167487737 is the quantile values with probability of 1e-16
    # for the standard Gumbel (max.) distribution (mu = 0.0, beta = 1.0)
    lower_bound = float(parameters[0] - 3.606621167487737 * parameters[1])

    return lower_bound


def upper(parameters: ARRAY_FLOAT):
    """Get the upper bound of a Gumbel (max.) distribution.

    Parameters
    ----------
    parameters : ARRAY_FLOAT
        The parameters of a Gumbel (max.) distribution.

    Returns
    -------
    float
        The upper bound of the Gumbel (max.) distribution.

    Notes
    -----
    - Strictly speaking, a Gumbel (max.) distribution is unbounded on both
      sides. However, for numerical reason a lower bound is set.
    - The difference between 1.0 and probability mass contained up to the
      upper bound of the Gumbel (max.) distribution is smaller than 1e-15.
    - The difference between 1.0 and the probability mass between lower and
      upper bounds is smaller than 1e-15.
    """
    # 36.7368005696771 is the quantile values with probability of 1-1e-16
    # for the standard Gumbel (max.) distribution (mu = 0.0, beta = 1.0)
    upper_bound = float(parameters[0] + 36.7368005696771 * parameters[1])

    return upper_bound


def pdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of a Gumbel (max.) distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a Gumbel (max.) distribution.
    parameters : ARRAY_FLOAT
        Parameters of the Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of the Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of the Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        PDF values of the Gumbel (max.) distribution on the sample values.

    Notes
    -----
    - The PDF for sample with values outside the bounds are set to 0.0.
    """
    idx_non_zero = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    # Get the parameters
    mu = parameters[0]
    beta = parameters[1]

    yy = np.zeros(xx.shape)
    yy[idx_non_zero] = gumbel_r.pdf(xx[idx_non_zero], loc=mu, scale=beta)

    return yy


def cdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of a Gumbel (max.) distribution.

    Parameters
    ----------
    xx : ARRAY_FLOAT
        Sample values (realizations) of a Gumbel (max.) distribution.
    parameters : ARRAY_FLOAT
        Parameters of the Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of the Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of the Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        CDF values of the Gumbel (max.) distribution on the sample values.

    Notes
    -----
    - CDF for sample with values smaller (resp. larger) than the lower bound
      (resp. upper bound) are set to 0.0 (resp. 1.0).
    """

    # Get the parameters
    mu = parameters[0]
    beta = parameters[1]

    yy = np.empty(xx.shape)

    # Set CDF to 0.0 for values below the lower bound
    idx_lower = xx < lower_bound
    yy[idx_lower] = 0.0

    # Set CDF to 1.0 for values above the upper bound
    idx_upper = xx > upper_bound
    yy[idx_upper] = 1.0

    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )
    yy[idx_rest] = gumbel_r.cdf(xx[idx_rest], loc=mu, scale=beta)

    return yy


def icdf(
    xx: ARRAY_FLOAT,
    parameters: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the ICDF values of a Gumbel (max.) distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of a Gumbel (max.) distribution.
    lower_bound : float
        Lower bound of a Gumbel (max.) distribution.
    upper_bound : float
        Upper bound of a Gumbel (max.) distribution.

    Returns
    -------
    ARRAY_FLOAT
        Transformed values in the domain of the Gumbel (max.) distribution.

    Notes
    -----
    - ICDF for sample values outside [0.0, 1.0] is set to NaN according to
      the underlying SciPy implementation.
    """
    # Get the parameters
    mu = parameters[0]
    beta = parameters[1]

    # Compute the ICDF
    yy = gumbel_r.ppf(xx, loc=mu, scale=beta)

    # Check if values are within the set bounds
    yy = postprocess_icdf(yy, lower_bound, upper_bound)

    return yy
