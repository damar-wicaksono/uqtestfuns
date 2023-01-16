"""
Module with routines involving the Gumbel maximum probability distribution.

The Gumbel distribution in UQTestFuns is parameterized by two parameters:
mu and beta.

The underlying implementation is based on the implementation from scipy.stats
(specifically, ``gumbel_r``  the right-skewed Gumbel).
In the SciPy convention, the parameter mu corresponds to the ``loc`` parameter,
while the parameter beta corresponds to the ``scale`` parameter.
"""
import numpy as np

from scipy.stats import gumbel_r

from ....global_settings import ARRAY_FLOAT

DISTRIBUTION_NAME = "gumbel"


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
    if parameters.size != 2:
        raise ValueError(
            f"A {DISTRIBUTION_NAME} distribution requires two parameters!"
            f"Expected 2, got {parameters.size}."
        )

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
      distribution is smaller than 1e-15.
    - The difference between 1.0 and the probability mass between lower and
      upper bounds is smaller than 1e-15.
    """
    # 3.6 is picked such that the probability mass (of a standard Gumbel)
    # up to the bound is less than 1e-15.
    lower_bound = float(parameters[0] - 3.6 * parameters[1])

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
    # 36 is picked such that the probability mass (of a standard Gumbel)
    # above the upper bound is less than 1e-15.
    upper_bound = float(parameters[0] + 36 * parameters[1])

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

    yy = np.zeros(xx.shape)
    mu = parameters[0]
    beta = parameters[1]

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
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    mu = parameters[0]
    beta = parameters[1]

    yy = np.empty(xx.shape)
    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
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
    - ICDF for sample with values of 0.0 and 1.0 are automatically set to the
      lower bound and upper bound, respectively.
    TODO: values outside [0, 1] must either be an error or NaN
    """
    idx_lower = xx == 0.0
    idx_upper = xx == 1.0
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    mu = parameters[0]
    beta = parameters[1]

    yy = np.empty(xx.shape)
    yy[idx_lower] = lower_bound
    yy[idx_upper] = upper_bound
    yy[idx_rest] = gumbel_r.ppf(xx[idx_rest], loc=mu, scale=beta)

    return yy
