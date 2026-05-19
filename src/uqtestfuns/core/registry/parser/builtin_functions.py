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
