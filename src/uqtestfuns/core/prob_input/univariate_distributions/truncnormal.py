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


DISTRIBUTION_NAME = "truncnormal"


def _get_parameters(parameters: np.ndarray) -> tuple:
    """Get the parameters of a truncated normal dist. w/ intuitive names.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a truncated normal distribution.

    Returns
    -------
    tuple
        The mean, standard deviation, lower bound, and upper bound of the
        truncated normal distribution.
    """
    mu = parameters[0]
    sigma = parameters[1]
    lb = parameters[2]
    ub = parameters[3]

    return mu, sigma, lb, ub


def verify_parameters(parameters: np.ndarray):
    """Verify the parameters of a truncated normal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a truncated normal distribution
        (i.e., the mean, standard deviation, and the lower and upper bounds).

    Returns
    ------
    None

    Raises
    ------
    ValueError
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    # Check overall shape
    if parameters.size != 4:
        raise ValueError(
            f"A truncated normal distribution requires four parameters!"
            f"Expected 4, got {parameters.size}."
        )

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

    if lb >= mu or ub <= mu:
        raise ValueError(
            f"The mean {mu} "
            f"must be between the bounds [{lb}, {ub}]!"
        )


def lower(parameters: np.ndarray) -> float:
    """Get the lower bound of a truncated normal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a truncated normal distribution.

    Returns
    -------
    float
        The lower bound of the truncated normal distribution.
    """
    _, _, lower_bound, _ = _get_parameters(parameters)

    return lower_bound


def upper(parameters: np.ndarray) -> float:
    """Get the upper bound of a truncated normal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of a truncated normal distribution

    Returns
    -------
    float
        The upper bound of the truncated normal distribution.
    """
    _, _, _, upper_bound = _get_parameters(parameters)

    return upper_bound


def pdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the PDF values of a truncated normal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a truncated normal distribution.
    parameters : np.ndarray
        Parameters of the truncated normal distribution.
    lower_bound : float
        Lower bound of the truncated normal distribution.
    upper_bound : float
        Upper bound of the truncated normal distribution.

    Returns
    -------
    np.ndarray
        PDF values of the truncated normal distribution on the sample values.

    Notes
    -----
    - The values outside the bounds are set to 0.0.
    - ``lower_bound`` and ``upper_bound`` in the function parameters are the
      same as the ones in ``parameters``. For a truncated normal distribution,
      the bounds are part of the parameterization.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    mu, sigma, lb_param, ub_param = _get_parameters(parameters)

    yy[idx] = truncnorm.pdf(
        xx[idx],
        a=(lb_param - mu)/sigma,
        b=(ub_param - mu)/sigma,
        loc=mu,
        scale=sigma
    )

    return yy


def cdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the CDF values of the truncated normal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a truncated normal distribution.
    parameters : np.ndarray
        Parameters of the truncated normal distribution.
    lower_bound : np.ndarray
        Lower bound of the truncated normal distribution.
    upper_bound : np.ndarray
        Upper bound of the truncated normal distribution.

    Returns
    -------
    np.ndarray
        CDF values of the truncated normal distribution on the sample values.

    Notes
    -----
    - CDF for sample with values smaller (resp. larger) than the lower bound
      (resp. upper bound) are set to 0.0 (resp. 1.0).
    - ``lower_bound`` and ``upper_bound`` in the function parameters are the
      same as the ones in ``parameters``. For a truncated normal distribution,
      the bounds are part of the parameterization.
    """
    yy = np.empty(xx.shape)
    idx_lower = xx < lower_bound
    idx_upper = xx > upper_bound
    idx_rest = np.logical_and(
        np.logical_not(idx_lower), np.logical_not(idx_upper)
    )

    mu, sigma, lb_param, ub_param = _get_parameters(parameters)

    yy[idx_lower] = 0.0
    yy[idx_upper] = 1.0
    yy[idx_rest] = truncnorm.cdf(
        xx[idx_rest],
        a=(lb_param - mu)/sigma,
        b=(ub_param - mu)/sigma,
        loc=mu,
        scale=sigma
    )

    return yy


def icdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
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
    np.ndarray
        Transformed values in the domain of the truncated normal distribution.

    Notes
    -----
    - ICDF for sample with values of 0.0 and 1.0 are automatically set to the
      lower bound and upper bound, respectively.
    - ``lower_bound`` and ``upper_bound`` in the function parameters are the
      same as the ones in ``parameters``. For a truncated normal distribution,
      the bounds are part of the parameterization.
    """
    yy = np.zeros(xx.shape)
    idx_lower = xx == 0.0
    idx_upper = xx == 1.0
    idx_rest = np.logical_not(idx_upper)

    mu, sigma, lb_param, ub_param = _get_parameters(parameters)

    yy[idx_lower] = lower_bound
    yy[idx_upper] = upper_bound
    yy[idx_rest] = truncnorm.ppf(
        xx[idx_rest],
        a=(lb_param - mu)/sigma,
        b=(ub_param - mu)/sigma,
        loc=mu,
        scale=sigma
    )

    return yy
