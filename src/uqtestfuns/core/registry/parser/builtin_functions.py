import numpy as np


def gumbel_max_beta(std: float) -> float:
    """Get the beta (scale) parameter of the Gumbel (max) distribution.

    Parameters
    ----------
    std : float
        The standard deviation of a Gumbel (max) distribution.

    Returns
    -------
    float
        The beta (scale) parameter of the Gumbel (max) distribution.
    """
    beta = std * np.sqrt(6) / np.pi

    return beta


def gumbel_max_mu(mean: float, std: float) -> float:
    """Get the mu (location) parameter of a Gumbel (max) distribution.

    Parameters
    ----------
    mean : float
        The mean of a Gumbel (max) distribution.
    std : float
        The standard deviation of a Gumbel (max) distribution.

    Returns
    -------
    float
        The mu (location) parameter of the Gumbel (max.) distribution.
    """
    beta = gumbel_max_beta(std)

    mu = mean - beta * np.euler_gamma

    return mu


def lognormal_sigma(lognormal_mean: float, lognormal_std: float) -> float:
    """Get the std of the underlying normal distribution of a lognormal dist.

    Parameters
    ----------
    lognormal_mean : float
        The mean of a lognormal distribution.
    lognormal_std : float
        The standard deviation of a lognormal distribution.

    Returns
    -------
    float
        The standard deviation of the underlying normal distribution.

    Notes
    -----
    - The logarithm of a lognormal distribution gives the underlying normal
      distribution.
    """
    normal_var = np.log(
        (lognormal_mean**2 + lognormal_std**2) / lognormal_mean**2
    )

    return np.sqrt(normal_var)


def lognormal_mu(lognormal_mean: float, lognormal_std: float) -> float:
    """Get the mean of the underlying normal distribution of a lognormal dist.

    Parameters
    ----------
    lognormal_mean : float
        The mean of a lognormal distribution.
    lognormal_std : float
        The standard deviation of a lognormal distribution.

    Returns
    -------
    float
        The mean of the underlying normal distribution.

    Notes
    -----
    - The logarithm of a lognormal distribution gives the underlying normal
      distribution.
    """
    normal_std = lognormal_sigma(lognormal_mean, lognormal_std)

    normal_mean = np.log(lognormal_mean) - normal_std**2 / 2.0

    return normal_mean
