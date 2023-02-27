"""
Test module specifically for UnivariateInput instances with logitnormal dist.
"""
import pytest
import numpy as np

from scipy.special import expit as logistic

from uqtestfuns.core.prob_input.univariate_distribution import UnivDist
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(5)
    distribution = "logitnormal"
    # Lognormal distribution expects 2 parameters not 3!
    parameters = np.sort(np.random.rand(3))

    with pytest.raises(ValueError):
        UnivDist(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    name = create_random_alphanumeric(10)
    distribution = "logitnormal"
    # The 2nd parameter of the lognormal distribution must be stricly positive!
    parameters = [7.71, -10]

    with pytest.raises(ValueError):
        UnivDist(
            name=name, distribution=distribution, parameters=parameters
        )


def test_get_pdf_values() -> None:
    """Test the PDF values from an instance of UnivariateInput."""

    name = create_random_alphanumeric(5)
    distribution = "logitnormal"
    parameters = np.sort(np.random.rand(2))

    my_univariate_input = UnivDist(
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


def test_median() -> None:
    """Test the median values from an instance of UnivariateInput."""
    name = create_random_alphanumeric(5)
    distribution = "logitnormal"
    parameters = np.sort(np.random.rand(2))

    my_univariate_input = UnivDist(
        name=name, distribution=distribution, parameters=parameters
    )

    sample_size = 1000000
    xx = my_univariate_input.get_sample(sample_size)

    median = np.median(xx)
    # Reference median is the logistic of the mean
    median_ref = logistic(parameters[0])

    assert np.isclose(median, median_ref, rtol=1e-03, atol=1e-03)
