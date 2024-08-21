"""
Utility module for probabilistic input modeling.
"""

from numpy.typing import ArrayLike
from types import ModuleType
from typing import Tuple

from .univariate_distributions import (
    beta,
    exponential,
    normal,
    gumbel,
    lognormal,
    triangular,
    trunc_gumbel,
    trunc_normal,
    logitnormal,
    uniform,
)
from ...global_settings import ARRAY_FLOAT

SUPPORTED_MARGINALS = {
    beta.DISTRIBUTION_NAME: beta,
    exponential.DISTRIBUTION_NAME: exponential,
    lognormal.DISTRIBUTION_NAME: lognormal,
    normal.DISTRIBUTION_NAME: normal,
    gumbel.DISTRIBUTION_NAME: gumbel,
    triangular.DISTRIBUTION_NAME: triangular,
    trunc_gumbel.DISTRIBUTION_NAME: trunc_gumbel,
    trunc_normal.DISTRIBUTION_NAME: trunc_normal,
    logitnormal.DISTRIBUTION_NAME: logitnormal,
    uniform.DISTRIBUTION_NAME: uniform,
}


def get_distribution_module(
    distribution: str,
) -> ModuleType:  # pragma: no cover
    """Get the relevant module corresponding to the distribution."""

    distribution_module = SUPPORTED_MARGINALS[distribution]

    return distribution_module


def verify_distribution(distribution: str) -> None:
    """Verify the type of distribution.

    Parameters
    ----------
    distribution : str
        Type of the distribution.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the type of distribution is not currently supported.
    """
    if distribution not in SUPPORTED_MARGINALS:
        raise ValueError(
            f"Univariate distribution {distribution!r} is not supported!"
        )


def get_distribution_bounds(
    distribution: str, parameters: ArrayLike
) -> Tuple[float, float]:
    """Get the bounds of the distribution given the parameters.

    While the support of many continuous density functions are unbounded,
    numerically they are always bounded. Below and above the bounds the density
    values are always zero.
    """
    distribution_module = get_distribution_module(distribution)
    lower = distribution_module.lower(parameters)
    upper = distribution_module.upper(parameters)

    return lower, upper


def verify_parameters(distribution: str, parameters: ArrayLike) -> None:
    """Verify the parameter values of the distribution"""
    distribution_module = get_distribution_module(distribution)

    distribution_module.verify_parameters(parameters)


def get_pdf_values(
    xx: ArrayLike,
    distribution: str,
    parameters: ArrayLike,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the PDF values of the distribution on a set of sample points.

    Notes
    -----
    - PDF stands for "probability density function".
    """
    distribution_module = get_distribution_module(distribution)
    out: ARRAY_FLOAT = distribution_module.pdf(
        xx, parameters, lower_bound, upper_bound
    )

    return out


def get_cdf_values(
    xx: ArrayLike,
    distribution: str,
    parameters: ArrayLike,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the CDF values of the distribution on a set of sample points.

    Notes
    -----
    - CDF stands for "cumulative distribution function".
    """
    distribution_module = get_distribution_module(distribution)
    out: ARRAY_FLOAT = distribution_module.cdf(
        xx, parameters, lower_bound, upper_bound
    )

    return out


def get_icdf_values(
    xx: ArrayLike,
    distribution: str,
    parameters: ArrayLike,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Get the inverse CDF values of the dist. on a set of sample points.

    Notes
    -----
    - CDF stands for "cumulative distribution function".
    - ICDF stands for "inverse cumulative distribution function".
    """
    distribution_module = get_distribution_module(distribution)
    out: ARRAY_FLOAT = distribution_module.icdf(
        xx, parameters, lower_bound, upper_bound
    )

    return out
