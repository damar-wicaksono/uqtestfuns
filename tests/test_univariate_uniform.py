"""
Test module specifically for UnivariateInput instances with uniform dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_parameters():
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = "uniform"
    # Uniform distribution expects 2 parameters not 1!
    parameters = np.sort(np.random.rand(1))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification():
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = "uniform"
    # The lower bound must be smaller than upper bound!
    parameters = [10, -10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_get_pdf_values():
    """Test the PDF values from an instance of UnivariateInput."""

    name = create_random_alphanumeric(5)
    distribution = "uniform"
    parameters = np.sort(np.random.rand(2))

    my_univariate_input = UnivariateInput(name, distribution, parameters)

    sample_size = 1000
    xx = my_univariate_input.get_sample(sample_size)

    # Assertions (PDF values of zero at the boundaries)
    assert np.all(
        np.logical_and(
            my_univariate_input.pdf(xx)
            >= my_univariate_input.pdf(my_univariate_input.lower),
            my_univariate_input.pdf(xx)
            >= my_univariate_input.pdf(my_univariate_input.upper),
        )
    )
