"""
Test module specifically for UnivDist instances with the exponential dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_distribution import UnivDist
from conftest import create_random_alphanumeric

DISTRIBUTION = "exponential"


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(5)
    # The distribution expects exactly 1 parameter!
    num_params = np.random.randint(2, 10)
    parameters = np.random.rand(num_params)

    with pytest.raises(ValueError):
        UnivDist(name=name, distribution=DISTRIBUTION, parameters=parameters)


def test_failed_parameter_verification() -> None:
    name = create_random_alphanumeric(10)
    # The parameter of an exponential distribution must be stricly positive!
    parameters = [-5]

    with pytest.raises(ValueError):
        UnivDist(name=name, distribution=DISTRIBUTION, parameters=parameters)


def test_get_pdf_values() -> None:
    """Test the PDF values from an instance of UnivDist."""

    name = create_random_alphanumeric(5)
    parameters = np.sort(np.random.rand(1))

    my_univariate_input = UnivDist(
        name=name, distribution=DISTRIBUTION, parameters=parameters
    )

    sample_size = 1000
    xx = my_univariate_input.get_sample(sample_size)

    # Assertions (PDF values are max. at the left bound and min. at the right)
    assert np.all(
        np.logical_and(
            my_univariate_input.pdf(xx)
            <= my_univariate_input.pdf(my_univariate_input.lower),
            my_univariate_input.pdf(xx)
            >= my_univariate_input.pdf(my_univariate_input.upper),
        )
    )


def test_mean() -> None:
    """Test the mean values from an instance of UnivDist."""
    name = create_random_alphanumeric(5)
    parameters = np.sort(np.random.rand(1))

    my_univariate_input = UnivDist(
        name=name, distribution=DISTRIBUTION, parameters=parameters
    )

    sample_size = 10000000
    xx = my_univariate_input.get_sample(sample_size)

    mean = np.mean(xx)
    mean_ref = 1 / parameters[0]

    assert np.isclose(mean, mean_ref, rtol=1e-02, atol=1e-02)


def test_variance() -> None:
    """Test the variance values from an instance of UnivDist."""
    name = create_random_alphanumeric(5)
    parameters = np.sort(np.random.rand(1))

    my_univariate_input = UnivDist(
        name=name, distribution=DISTRIBUTION, parameters=parameters
    )

    sample_size = 10000000
    xx = my_univariate_input.get_sample(sample_size)

    var = np.var(xx)
    var_ref = 1 / (parameters[0] ** 2)

    assert np.isclose(var, var_ref, rtol=1e-02, atol=1e-02)


def test_median() -> None:
    """Test the median values from an instance of UnivDist."""
    name = create_random_alphanumeric(5)
    parameters = np.sort(np.random.rand(1))

    my_univariate_input = UnivDist(
        name=name, distribution=DISTRIBUTION, parameters=parameters
    )

    sample_size = 10000000
    xx = my_univariate_input.get_sample(sample_size)

    median = np.median(xx)
    median_ref = np.log(2) / parameters[0]

    assert np.isclose(median, median_ref, rtol=1e-02, atol=1e-02)
