"""
Test module specifically for UnivariateInput instances with Gumbel (max.)
distribution.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_distribution import UnivDist
from uqtestfuns.global_settings import ARRAY_FLOAT
from conftest import create_random_alphanumeric

DISTRIBUTION_NAME = "gumbel"


def _calc_mean(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical mean of a Gumbel (max.) distribution."""
    mu, beta = parameters[:]

    mean = mu + beta * np.euler_gamma

    return mean


def _calc_mode(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical mode of a Gumbel (max.) distribution."""
    mu, _ = parameters[:]

    return mu


def _calc_median(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical median of a Gumbel (max.) distribution."""
    mu, beta = parameters[:]

    median = mu - beta * np.log(np.log(2))

    return median


def _calc_variance(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical variance of a Gumbel (max.) distribution."""
    mu, beta = parameters[:]

    var = np.pi**2 / 6.0 * beta**2

    return var


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = DISTRIBUTION_NAME
    # Gumbel distribution expects 2 parameters not 5!
    parameters = np.sort(np.random.rand(5))

    with pytest.raises(ValueError):
        UnivDist(name=name, distribution=distribution, parameters=parameters)


def test_failed_parameter_verification() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME
    # The 2nd parameter of the Gumbel (max.) dist. must be strictly positive!
    parameters = [7.71, -5.0]

    with pytest.raises(ValueError):
        UnivDist(name=name, distribution=distribution, parameters=parameters)


def test_estimate_mean() -> None:
    """Test the mean estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(2))

    # Create an instance
    my_univariate_input = UnivDist(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-2 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    mean = np.mean(xx)

    # Analytical result
    mean_ref = _calc_mean(parameters)

    # Assertion
    assert np.isclose(mean, mean_ref, rtol=1e-2, atol=1e-2)


def test_estimate_variance() -> None:
    """Test the variance estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(2))

    # Create an instance
    my_univariate_input = UnivDist(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-2 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    var = np.var(xx)

    # Analytical result
    var_ref = _calc_variance(parameters)

    # Assertion
    assert np.isclose(var, var_ref, rtol=1e-2, atol=1e-2)


def test_estimate_median() -> None:
    """Test the median estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(2))

    # Create an instance
    my_univariate_input = UnivDist(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-2 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    median = np.median(xx)

    # Analytical result
    median_ref = _calc_median(parameters)

    # Assertion
    assert np.isclose(median, median_ref, rtol=1e-2, atol=1e-2)


def test_estimate_mode() -> None:
    """Test the mode estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(2))

    # Create an instance
    my_univariate_input = UnivDist(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-0 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    y, edges = np.histogram(xx, bins="auto")
    mode = edges[np.argmax(y)]

    # Analytical result
    mode_ref = _calc_mode(parameters)

    # Assertion
    assert np.isclose(mode, mode_ref, rtol=1, atol=1)
