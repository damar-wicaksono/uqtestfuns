"""
Module with routines involving uniform density functions.

The uniform distribution in UQTestFuns is parametrized by its lower and upper
bounds.
"""
import numpy as np


DISTRIBUTION_NAME = "uniform"


def verify_parameters(parameters: np.ndarray):
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
        If any of the parameter values are invalid
        or the shapes are inconsistent.
    """
    if parameters.size != 2:
        raise ValueError(
            f"A uniform distribution requires two parameters!"
            f"Expected 2, got {parameters.size}."
        )

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
        The parameters of the uniform distribution.

    Returns
    -------
    float
        The lower bound of the uniform distribution.
    """
    lower_bound = parameters[0]

    return lower_bound


def upper(parameters: np.ndarray) -> float:
    """Get the upper bound of the uniform distribution.

    Parameters
    ----------
    parameters : np.ndarray
        The parameters of the uniform distribution.

    Returns
    -------
    float
        The upper bound of the uniform distribution.
    """
    upper_bound = parameters[1]

    return upper_bound


def pdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the PDF values of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a uniform distribution.
    parameters : np.ndarray
        Parameters of the uniform distribution.
    lower_bound: float
        Lower bound of the uniform distribution.
    upper_bound: float
        Upper bound of the distribution.

    Returns
    -------
    np.ndarray
        The PDF values of the uniform distribution.

    Notes
    -----
    - The sample values `xx` themselves are not used in the computation of
      density value (it is a constant), but required nevertheless as
      the function is vectorized.
      Given a vector input it should return the PDF values of the same length
      as the input. Furthermore, this signature is consistent with
      the other distributions.
    - The values outside the bounds are set to 0.0.
    """
    yy = np.zeros(xx.shape)
    idx = np.logical_and(xx >= lower_bound, xx <= upper_bound)

    yy[idx] = 1 / (np.diff(parameters))

    return yy


def cdf(
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the CDF values of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) of a uniform distribution.
    parameters : np.ndarray
        Parameters of the uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution
    upper_bound : float
        Upper bound of the uniform distribution.

    Returns
    -------
    np.ndarray
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
        xx: np.ndarray,
        parameters: np.ndarray,
        lower_bound: float,
        upper_bound: float
) -> np.ndarray:
    """Get the inverse CDF values of a uniform distribution.

    Parameters
    ----------
    xx : np.ndarray
        Sample values (realizations) in the [0, 1] domain.
    parameters : np.ndarray
        Parameters of the uniform distribution.
    lower_bound : float
        Lower bound of the uniform distribution.
        This parameter is not used but must appear for interface consistency.
    upper_bound : float
        Upper bound of the uniform distribution.
        This parameter is not used but must appear for interface consistency.

    Returns
    -------
    np.ndarray
        Transformed values in the domain of the uniform distribution.
    """
    yy = parameters[0] + np.diff(parameters) * xx

    return yy
