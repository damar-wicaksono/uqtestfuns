"""
Test module for UnivariateInput instances.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from uqtestfuns.core.prob_input.utils import SUPPORTED_MARGINALS
from conftest import create_random_alphanumeric


MARGINALS = list(SUPPORTED_MARGINALS.keys())


@pytest.fixture(params=MARGINALS)
def univariate_input(request):
    """Test fixture, an instance of UnivariateInput."""
    name = create_random_alphanumeric(8)
    distribution = request.param
    if request.param == "uniform":
        parameters = np.sort(np.random.rand(2))
    elif request.param == "beta":
        parameters = np.sort(np.random.rand(4))
    elif distribution == "truncnormal":
        # mu must be inside the bounds
        parameters = np.sort(1 + 2 * np.random.rand(3))
        parameters[[0, 1]] = parameters[[1, 0]]
        # Insert sigma as the second parameter
        parameters = np.insert(parameters, 1, np.random.rand(1))
    elif distribution == "lognormal":
        # Limit the size of the parameters
        parameters = 1 + np.random.rand(2)
    else:
        parameters = 5 * np.random.rand(2)
        parameters[1] += 1.0

    specs = {
        "name": name,
        "distribution": distribution,
        "parameters": parameters,
    }

    my_univariate_input = UnivariateInput(**specs)

    return my_univariate_input, specs


def test_create_instance(univariate_input):
    """Test the creation of instance with np.array as params."""

    my_univariate_input, specs = univariate_input

    assert my_univariate_input.name == specs["name"]
    assert my_univariate_input.distribution == specs["distribution"].lower()
    assert np.allclose(my_univariate_input.parameters, specs["parameters"])


def test_create_instance_unsupported_marginal():
    """Test the creation of an instance with an unsupported marginal."""
    name = create_random_alphanumeric(10)
    distribution = create_random_alphanumeric(10)
    parameters = list(np.sort(np.random.rand(2)))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_generate_sample(univariate_input):
    """Test sample generation from an instance of UnivariateInput."""

    my_univariate_input, _ = univariate_input

    sample_size = 1000
    xx = my_univariate_input.get_sample(sample_size)

    assert len(xx) == sample_size  # Test the length
    assert np.min(xx) >= my_univariate_input.lower  # Test the lower bound
    assert np.max(xx) <= my_univariate_input.upper  # Test the upper bound


def test_get_pdf_values(univariate_input):
    """Test the PDF values from an instance of UnivariateInput."""

    my_univariate_input, _ = univariate_input

    # Assertions
    assert my_univariate_input.pdf(my_univariate_input.lower - 0.1) <= 1e-15
    assert my_univariate_input.pdf(my_univariate_input.upper + 0.1) <= 1e-15


def test_get_cdf_values(univariate_input):
    """Test the CDF values from an instance of UnivariateInput."""

    my_univariate_input, _ = univariate_input

    sample_size = 10000
    xx = my_univariate_input.get_sample(sample_size)
    cdf_values = my_univariate_input.cdf(xx)

    # Assertions
    assert np.min(cdf_values) >= 0.0  # Test the lower bound of sampled CDF
    assert np.max(cdf_values) <= 1.0  # Test the upper bound of sampled CDF
    assert np.isclose(
        my_univariate_input.cdf(my_univariate_input.lower), 0.0
    )  # Test the lower bound of CDF
    assert np.isclose(
        my_univariate_input.cdf(my_univariate_input.upper), 1.0
    )  # Test the upper bound of CDF


def test_get_icdf_values(univariate_input):
    """Test the inverse CDF values from an instance of UnivariateInput."""
    my_univariate_input, _ = univariate_input

    sample_size = 10000
    xx = np.random.rand(sample_size)
    icdf_values = my_univariate_input.icdf(xx)

    # Assertions
    # Test the lower bound of sampled ICDF
    assert np.min(icdf_values) >= my_univariate_input.lower
    # Test the upper bound of sampled ICDF
    assert np.max(icdf_values) <= my_univariate_input.upper
    # Test the lower bound of ICDF
    assert np.isclose(my_univariate_input.icdf(0.0), my_univariate_input.lower)
    # Test the upper bound of ICDF
    assert np.isclose(my_univariate_input.icdf(1.0), my_univariate_input.upper)


def test_transform_sample():
    """Test the transformation of sample values from one dist. to another."""
    name_1 = create_random_alphanumeric(5)
    distribution_1 = "uniform"
    parameters_1 = np.sort(np.random.rand(2))

    my_univariate_input_1 = UnivariateInput(
        name=name_1, distribution=distribution_1, parameters=parameters_1
    )

    sample_size = 5000
    xx = my_univariate_input_1.get_sample(sample_size)

    name_2 = create_random_alphanumeric(5)
    distribution_2 = "uniform"
    parameters_2 = np.sort(np.random.rand(2))

    my_univariate_input_2 = UnivariateInput(
        name=name_2, distribution=distribution_2, parameters=parameters_2
    )

    xx_trans = my_univariate_input_1.transform_sample(
        xx, my_univariate_input_2
    )

    # Assertions
    assert np.min(xx_trans) >= my_univariate_input_2.lower
    assert np.max(xx_trans) <= my_univariate_input_2.upper


def test_failed_transform_sample():
    """Test the failure of sample transformation."""
    name = create_random_alphanumeric(5)
    distribution = "uniform"
    parameters = np.sort(np.random.rand(2))

    my_univariate_input = UnivariateInput(
        name=name, distribution=distribution, parameters=parameters
    )

    sample_size = 1000
    xx = my_univariate_input.get_sample(sample_size)

    with pytest.raises(TypeError):
        my_univariate_input.transform_sample(xx, [])
