"""
Module with computations involving uniform density functions.
"""
import numpy as np


def verify_parameters(parameters: np.ndarray) -> float:
    """Verify the parameters of a uniform distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the uniform distribution
        (i.e., lower and upper bounds).

    Returns
    ------
    None

    Raises
    ------
    ValueError
        If any of the parameter values are invalid.
    """
    if parameters[0] >= parameters[1]:
        raise ValueError(
            f"The lower bound {parameters[0]} "
            f"cannot be greater than the upper bound {parameters[1]}!"
        )


def lower(parameters: np.ndarray) -> float:
    """Get the lower bound of the uniform distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the uniform distribution
        (i.e., lower and upper bounds).

    Returns
    -------
    float
        The lower bound of the uniform distribution.
    """
    return parameters[0]


def upper(parameters: np.ndarray) -> float:
    """Get the upper bound of the uniform distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the uniform distribution
        (i.e., lower and upper bounds).

    Returns
    -------
    float
        The upper bound of the uniform distribution.
    """
    return parameters[1]


def pdf(xx: np.ndarray, parameters: np.ndarray):
    """Get the PDF value of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a uniform distribution.
    parameters : np.ndarray
        Parameters of the uniform distribution.

    Notes
    -----
    - The sample values `xx` themselves are not used in the computation of
      density value (it is a constant), but required nevertheless as
      the function is vectorized.
      Given a vector input it should return the PDF values of the same length
      as the input. Furthermore, this signature is consistent with
      the other distributions.
    """
    yy = np.tile(1 / (np.diff(parameters)), xx.shape)

    return yy


def cdf(xx: np.ndarray, parameters: np.ndarray):
    """Get the CDF value of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a uniform distribution.
    parameters : np.ndarray
        Parameters of the uniform distribution.
    """
    yy = (xx - parameters[0]) / np.diff(parameters)

    return yy


def icdf(xx: np.ndarray, parameters: np.ndarray):
    """Get the inverse CDF values of a uniform distribution.

    The function transform from the [0,1] domain to the domain
    of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of the uniform distribution.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the uniform distribution.
    """
    yy = parameters[0] + np.diff(parameters) * xx

    return yy
