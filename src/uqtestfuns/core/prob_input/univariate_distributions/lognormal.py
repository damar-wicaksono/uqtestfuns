"""
Module with routines involving lognormal density functions.

The lognormal distribution in UQTestFuns is parametrized by the parameters
lambda and xi, the mean and standard deviation of the corresponding normal
distribution, respectively.

The underlying implementation used the implementation from scipy.stats.
In scipy convention, the shape distribution ``s`` corresponds to the normal
distribution standard deviation, while the scale parameters corresponds to
the exponent of the normal distribution mean.
"""
import numpy as np
from scipy.stats import lognorm


def verify_parameters(parameters: np.ndarray) -> float:
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

    Raises
    ------
    ValueError
        If any of the parameter values are invalid or the shapes
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


def lower(parameters: np.ndarray) -> float:
    """Get the lower bound of the uniform distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the lognormal distribution.

    Returns
    -------
    float
        The lower bound of the uniform distribution.

    Notes
    -----
    - The parameters are not used in determining the lower bound of
      the distribution; it must, however, appear for interface consistency.
      The lower bound of a lognormal distribution is 0.0 and it is finite.
    """
    lower_bound = 0.0

    return lower_bound


def upper(parameters: np.ndarray) -> float:
    """Get the upper bound of the lognormal distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the uniform distribution

    Returns
    -------
    float
        The upper bound of the uniform distribution.

    Notes
    -----
    - Strictly speaking, a lognormal distribution is unbounded on the right.
      However, for numerical reason an upper bound is set.
    - The upper bound of the lognormal distribution is chosen such that
      the difference between 1.0 and the CDF from the lower bound to the upper
      bound is smaller than 1e-15.
    """
    upper_bound = float(np.exp(8.22 * parameters[1] + parameters[0]))

    return upper_bound


def pdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the PDF values of the lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a lognormal distribution.
    parameters : np.ndarray
        Parameters of the lognormal distribution.
    lower_bound : np.ndarray
        Lower bound of the lognormal distribution.
    upper_bound : np.ndarray
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
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the CDF values of the lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a lognormal distribution.
    parameters : np.ndarray
        Parameters of the lognormal distribution.
    lower_bound : np.ndarray
        Lower bound of the lognormal distribution.
    upper_bound : np.ndarray
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
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the inverse CDF values of a lognormal distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of the lognormal distribution.
    lower_bound : np.ndarray
        Lower bound of the lognormal distribution.
    upper_bound : np.ndarray
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
