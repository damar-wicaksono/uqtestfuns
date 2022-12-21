"""
Test module specifically for UnivariateInput instances with lognormal dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(5)
    distribution = "lognormal"
    # Lognormal distribution expects 2 parameters not 3!
    parameters = np.sort(np.random.rand(3))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    name = create_random_alphanumeric(10)
    distribution = "lognormal"
    # The 2nd parameter of the lognormal distribution must be stricly positive!
    parameters = [7.71, -10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_get_pdf_values() -> None:
    """Test the PDF values from an instance of UnivariateInput."""

    name = create_random_alphanumeric(5)
    distribution = "lognormal"
    parameters = np.sort(np.random.rand(2))

    my_univariate_input = UnivariateInput(
        name=name, distribution=distribution, parameters=parameters
    )

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
