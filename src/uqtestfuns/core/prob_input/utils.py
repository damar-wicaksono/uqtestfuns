"""
Utility module for probabilistic input modeling.
"""

from .univariate_distributions import (
    uniform,
    lognormal,
    normal,
    beta,
    truncnormal,
    logitnormal,
)

SUPPORTED_MARGINALS = {
    uniform.DISTRIBUTION_NAME: uniform,
    lognormal.DISTRIBUTION_NAME: lognormal,
    normal.DISTRIBUTION_NAME: normal,
    beta.DISTRIBUTION_NAME: beta,
    truncnormal.DISTRIBUTION_NAME: truncnormal,
    logitnormal.DISTRIBUTION_NAME: logitnormal,
}


def get_distribution_module(distribution: str):  # pragma: no cover
    """Get the relevant module corresponding to the distribution."""

    distribution_module = SUPPORTED_MARGINALS[distribution]

    return distribution_module


def verify_distribution(distribution: str):
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
            f"Univariate distribution '{distribution}' is not supported!"
        )


def get_distribution_bounds(distribution, parameters):
    """Get the bounds of the distribution given the parameters.

    While the support of many continuous density functions are unbounded,
    numerically they are always bounded. Below and above the bounds the density
    values are always zero.
    """
    distribution_module = get_distribution_module(distribution)
    lower = distribution_module.lower(parameters)
    upper = distribution_module.upper(parameters)

    return lower, upper


def verify_parameters(distribution, parameters):
    """Verify the parameter values of the distribution"""
    distribution_module = get_distribution_module(distribution)

    distribution_module.verify_parameters(parameters)


def get_pdf_values(xx, distribution, parameters, lower_bound, upper_bound):
    """Get the PDF values of the distribution on a set of sample points.

    Notes
    -----
    - PDF stands for "probability density function".
    """
    distribution_module = get_distribution_module(distribution)

    return distribution_module.pdf(xx, parameters, lower_bound, upper_bound)


def get_cdf_values(xx, distribution, parameters, lower_bound, upper_bound):
    """Get the CDF values of the distribution on a set of sample points.

    Notes
    -----
    - CDF stands for "cumulative distribution function".
    """
    distribution_module = get_distribution_module(distribution)

    return distribution_module.cdf(xx, parameters, lower_bound, upper_bound)


def get_icdf_values(xx, distribution, parameters, lower_bound, upper_bound):
    """Get the inverse CDF values of the dist. on a set of sample points.

    Notes
    -----
    - CDF stands for "cumulative distribution function".
    - ICDF stands for "inverse cumulative distribution function".
    """
    distribution_module = get_distribution_module(distribution)

    return distribution_module.icdf(xx, parameters, lower_bound, upper_bound)
