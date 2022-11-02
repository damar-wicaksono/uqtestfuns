"""
Test module for UnivariateInput instances with a Beta distribution.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def _mean(parameters: np.ndarray) -> float:
    """Compute the analytical mean of a Beta distribution."""
    mean = parameters[2] + (parameters[3] - parameters[2]) * (
        (parameters[0] / (parameters[0] + parameters[1]))
    )

    return mean


def _std(parameters: np.ndarray) -> float:
    """Compute the analytical standard deviation of a Beta distribution."""
    std = (
        (parameters[3] - parameters[2])
        / (parameters[0] + parameters[1])
        * np.sqrt(
            (parameters[0] * parameters[1])
            / (parameters[0] + parameters[1] + 1)
        )
    )

    return std


def test_wrong_number_of_parameters():
    """Test the failure when specifying invalid number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = "beta"
    # Beta distribution expects 4 parameters not 6!
    parameters = np.sort(np.random.rand(6))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification():
    """Test the failure when specifying the wrong parameter values"""
    name = create_random_alphanumeric(10)
    distribution = "beta"

    # The 1st parameter of the Beta distribution must be strictly positive!
    parameters = [-7.71, 10, 1, 2]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The 2nd parameter of the Beta distribution must be strictly positive!
    parameters = [7.71, -10, 1, 2]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The lower bound must be smaller than upper bound!
    parameters = [1, 2, 4, 3]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_estimate_mean():
    """Test the mean estimation of a Beta distribution."""

    # Create an instance of a Beta UnivariateInput
    name = create_random_alphanumeric(10)
    distribution = "beta"
    parameters = np.sort(2 * np.random.rand(4))

    my_univariate_input = UnivariateInput(name, distribution, parameters)

    sample_size = 100000
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    mean = np.mean(xx)

    # Analytical result
    mean_ref = _mean(parameters)

    # Assertion
    assert np.isclose(mean, mean_ref, rtol=1e-03, atol=1e-04)


def test_estimate_std():
    """Test the standard deviation estimation of a Beta distribution."""

    # Create an instance of a Beta UnivariateInput
    name = create_random_alphanumeric(10)
    distribution = "beta"
    parameters = np.sort(2 * np.random.rand(4))

    my_univariate_input = UnivariateInput(name, distribution, parameters)

    sample_size = 100000
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    std = np.std(xx)

    # Analytical result
    std_ref = _std(parameters)

    # Assertion
    assert np.allclose(std, std_ref, rtol=1e-03, atol=1e-04)
