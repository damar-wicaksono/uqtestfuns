"""
Test module for UnivariateInput instances with a truncated normal distribution.
"""
import pytest
import numpy as np

from scipy.stats import norm

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from uqtestfuns.global_settings import ARRAY_FLOAT
from conftest import create_random_alphanumeric


DISTRIBUTION_NAME = "trunc-normal"


def _calc_mean(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical mean of a given truncated normal distribution."""
    mu, sigma, lb, ub = parameters[:]

    alpha = (lb - mu) / sigma
    beta = (ub - mu) / sigma
    phi_alpha = norm.pdf(alpha)
    phi_beta = norm.pdf(beta)
    z = norm.cdf(beta) - norm.cdf(alpha)

    mean = mu - (phi_beta - phi_alpha) / z * sigma

    return float(mean)


def _calc_std(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical standard deviation of a given trunc. normal."""
    mu, sigma, lb, ub = parameters[:]

    alpha = (lb - mu) / sigma
    beta = (ub - mu) / sigma
    phi_alpha = norm.pdf(alpha)
    phi_beta = norm.pdf(beta)
    z = norm.cdf(beta) - norm.cdf(alpha)

    term_1 = 1
    term_2 = (beta * phi_beta - alpha * phi_alpha) / z
    term_3 = ((phi_beta - phi_alpha) / z) ** 2
    var = sigma**2 * (term_1 - term_2 - term_3)

    return float(np.sqrt(var))


def test_wrong_number_of_parameters() -> None:
    """Test the failure when specifying invalid number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = DISTRIBUTION_NAME
    # A truncated normal distribution expects 4 parameters not 6!
    parameters = np.sort(np.random.rand(6))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    """Test the failure when specifying the wrong parameter values"""
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME

    # The 2nd parameter of the Beta distribution must be strictly positive!
    parameters = [7.71, -10, 1, 2]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The mean must be inside the bounds!
    parameters = [5, 2, 1, 3]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The mean must be inside the bounds!
    parameters = [0, 2, 1, 3]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The lower bound must be smaller than upper bound!
    parameters = [3.5, 2, 4, 3]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_estimate_mean() -> None:
    """Test the mean estimation of a truncated normal distribution."""

    # Create an instance of a truncated normal UnivariateInput
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME
    # mu must be inside the bounds
    parameters = np.sort(1 + 2 * np.random.rand(3))
    parameters[[0, 1]] = parameters[[1, 0]]
    # Insert sigma as the second parameter
    parameters = np.insert(parameters, 1, np.random.rand(1))

    my_univariate_input = UnivariateInput(
        name=name, distribution=distribution, parameters=parameters
    )

    sample_size = 100000
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    mean = np.mean(xx)

    # Analytical result
    mean_ref = _calc_mean(parameters)

    # Assertion
    assert np.isclose(mean, mean_ref, rtol=5e-03, atol=5e-04)


def test_estimate_std() -> None:
    """Test the standard deviation estimation of a trunc. normal dist."""

    # Create an instance of a truncated normal UnivariateInput
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME
    # mu must be inside the bounds
    parameters = np.sort(1 + 2 * np.random.rand(3))
    parameters[[0, 1]] = parameters[[1, 0]]
    # Insert sigma as the second parameter
    parameters = np.insert(parameters, 1, np.random.rand(1))

    my_univariate_input = UnivariateInput(
        name=name, distribution=distribution, parameters=parameters
    )

    sample_size = 1000000
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    std = np.std(xx)

    # Analytical result
    std_ref = _calc_std(parameters)

    # Assertion
    assert np.isclose(std, std_ref, rtol=5e-03, atol=5e-04)


def test_untruncated() -> None:
    """When the bounds are set to inf, it must be the same to normal one."""

    # Create an instance of a truncated normal UnivariateInput
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME
    parameters = [10, 2, -np.inf, np.inf]

    my_univariate_input = UnivariateInput(
        name=name, distribution=distribution, parameters=parameters
    )

    # Create a reference normal distribution
    my_univariate_input_ref = UnivariateInput(
        distribution="normal", parameters=parameters[:2]
    )

    # Assertion
    # PDF
    xx = np.linspace(0, 20, 10000)
    yy = my_univariate_input.pdf(xx)
    yy_ref = my_univariate_input_ref.pdf(xx)
    assert np.allclose(yy, yy_ref)

    # CDF
    yy = my_univariate_input.cdf(xx)
    yy_ref = my_univariate_input_ref.cdf(xx)
    assert np.allclose(yy, yy_ref)

    # ICDF
    xx = np.linspace(0, 1, 10000)
    quantiles = my_univariate_input.icdf(xx)
    quantiles_ref = my_univariate_input_ref.icdf(xx)
    assert np.allclose(quantiles, quantiles_ref)
