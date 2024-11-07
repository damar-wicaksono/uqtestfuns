import pytest
import numpy as np

from uqtestfuns.core.prob_input.probabilistic_input import ProbInput
from conftest import create_random_marginals


@pytest.mark.parametrize("input_dimension", [1, 2, 10, 100])
def test_create_instance_numpy_parameters(input_dimension):
    """Test the creation of a MultivariateInput instance."""
    marginals = create_random_marginals(input_dimension)

    my_multivariate_input = ProbInput(marginals)

    # Assertions
    # Test the dimensionality
    assert my_multivariate_input.input_dimension == input_dimension
    for i in range(input_dimension):
        # Test the name of the marginals
        assert marginals[i].name == my_multivariate_input.marginals[i].name

        # Test the type of distributions
        assert (
            marginals[i].distribution
            == my_multivariate_input.marginals[i].distribution
        )
        # Test the parameter values
        assert np.all(
            marginals[i].parameters
            == my_multivariate_input.marginals[i].parameters
        )


@pytest.mark.parametrize("input_dimension", [1, 2, 10, 100])
def test_generate_sample(input_dimension):
    """Test sample generation from an instance of MultivariateInput."""
    marginals = create_random_marginals(input_dimension)

    my_multivariate_input = ProbInput(marginals)

    sample_size = 5325
    xx = my_multivariate_input.get_sample(sample_size)

    # Assertions
    # Test the number of sample points
    assert xx.shape[0] == sample_size
    # Test the dimensionality of the sample
    assert xx.shape[1] == input_dimension
    # Test the bounds
    for i in range(input_dimension):
        assert np.min(xx[:, i]) >= my_multivariate_input.marginals[i].lower
        assert np.max(xx[:, i]) <= my_multivariate_input.marginals[i].upper


def test_generate_dependent_sample():
    """Test dependent sample generation (not yet supported; raise error)."""
    marginals = create_random_marginals(5)

    my_multivariate_input = ProbInput(marginals, "a")

    with pytest.raises(ValueError):
        my_multivariate_input.get_sample(1000)


@pytest.mark.parametrize("input_dimension", [1, 5])
def test_get_pdf_values(input_dimension):
    """Test the PDF values from an instance of MultivariateInput."""
    marginals = create_random_marginals(input_dimension)

    my_multivariate_input = ProbInput(marginals)

    sample_size = 100
    xx = my_multivariate_input.get_sample(sample_size)
    pdf_values = my_multivariate_input.pdf(xx)

    # Assert the positiveness of the PDF value
    assert np.all(pdf_values >= 0)
    assert np.all(pdf_values < np.inf)


def test_get_dependent_pdf_values():
    """Test dependent PDF value computation (not yet supported)."""
    marginals = create_random_marginals(5)

    my_multivariate_input = ProbInput(marginals, "b")

    with pytest.raises(ValueError):
        my_multivariate_input.pdf(np.random.rand(2, 5))


@pytest.mark.parametrize("input_dimension", [1, 2, 10])
def test_transform_sample(input_dimension):
    """Test the transformation of sample values from one dist. to another."""
    marginals_1 = create_random_marginals(input_dimension)
    my_multivariate_input_1 = ProbInput(marginals_1)

    sample_size = 5000
    xx = my_multivariate_input_1.get_sample(sample_size)

    marginals_2 = create_random_marginals(input_dimension)
    my_multivariate_input_2 = ProbInput(marginals_2)

    xx_trans = my_multivariate_input_1.transform_sample(
        xx, my_multivariate_input_2
    )

    # Assertions
    for i, marginal in enumerate(my_multivariate_input_2.marginals):
        assert np.min(xx_trans[:, i]) >= marginal.lower
        assert np.max(xx_trans[:, i]) <= marginal.upper


def test_failed_transform_sample():
    """Test the failure of sample transformation for MultiVariateInput."""
    marginals_1 = create_random_marginals(5)
    my_multivariate_input_1 = ProbInput(marginals_1)

    marginals_2 = create_random_marginals(10)
    my_multivariate_input_2 = ProbInput(marginals_2)

    sample_size = 5000
    xx = my_multivariate_input_1.get_sample(sample_size)

    # Transformation between two random variables of different dimensions
    with pytest.raises(ValueError):
        my_multivariate_input_1.transform_sample(xx, my_multivariate_input_2)


def test_transform_dependent_sample():
    """Test dependent transformation (not yet supported; raise an error)."""
    marginals_1 = create_random_marginals(5)
    my_multivariate_input_1 = ProbInput(marginals_1, "a")

    marginals_2 = create_random_marginals(5)
    my_multivariate_input_2 = ProbInput(marginals_2)

    xx = np.random.rand(2, 5)

    with pytest.raises(ValueError):
        my_multivariate_input_1.transform_sample(xx, my_multivariate_input_2)


def test_str():
    """Test __str__ method of an instance of ProbInput."""
    # Create a test instance
    marginals = create_random_marginals(5)
    my_probinput = ProbInput(marginals)

    # Create a string
    my_str = my_probinput.__str__()

    # Assertion
    assert isinstance(my_str, str)


@pytest.mark.parametrize("input_dimension", [1, 2, 10, 100])
def test_pass_random_seed(input_dimension):
    """Test passing random seed to the constructor."""
    marginals = create_random_marginals(input_dimension)

    # Create two instances with an identical seed number
    rng_seed = 42
    my_input_1 = ProbInput(marginals, rng_seed=rng_seed)
    my_input_2 = ProbInput(marginals, rng_seed=rng_seed)

    # Generate sample points
    xx_1 = my_input_1.get_sample(1000)
    xx_2 = my_input_2.get_sample(1000)

    # Assertion: Both samples are identical because the seed is identical
    assert np.allclose(xx_1, xx_2)


@pytest.mark.parametrize("input_dimension", [1, 2, 10, 100])
def test_reset_rng(input_dimension):
    """Test resetting the RNG once an instance has been created."""
    marginals = create_random_marginals(input_dimension)

    # Create two instances with an identical seed number
    rng_seed = 42
    my_input = ProbInput(marginals, rng_seed=rng_seed)

    # Generate sample points
    xx_1 = my_input.get_sample(1000)
    xx_2 = my_input.get_sample(1000)

    # Assertion: Both samples should not be equal
    assert not np.allclose(xx_1, xx_2)

    # Reset the RNG and generate new sample points
    my_input.reset_rng(rng_seed)
    xx_2 = my_input.get_sample(1000)

    # Assertion: Both samples should now be equal
    assert np.allclose(xx_1, xx_2)


# def test_get_cdf_values():
#     """Test the CDF values from an instance of UnivariateInput."""
#     name = create_random_alphanumeric(10)
#     distribution = "uniform"
#     parameters = list(np.sort(np.random.rand(2)))
#
#     my_univariate_input = UnivariateInput(
#         name=name, distribution=distribution, parameters=parameters
#     )
#
#     sample_size = 10000
#     xx = my_univariate_input.get_sample(sample_size)
#     cdf_values = my_univariate_input.cdf(xx)
#
#     # Assertions
#     assert np.min(cdf_values) >= 0.0  # Test the lower bound of sampled CDF
#     assert np.max(cdf_values) <= 1.0  # Test the upper bound of sampled CDF
#     assert np.isclose(
#         my_univariate_input.cdf(my_univariate_input.lower), 0.0
#     )  # Test the lower bound of CDF
#     assert np.isclose(
#         my_univariate_input.cdf(my_univariate_input.upper), 1.0
#     )  # Test the upper bound of CDF
#
#
# def test_get_icdf_values():
#     """Test the inverse CDF values from an instance of UnivariateInput."""
#     name = create_random_alphanumeric(10)
#     distribution = "uniform"
#     parameters = np.sort(np.random.rand(2))
#
#     my_univariate_input = UnivariateInput(
#         name=name, distribution=distribution, parameters=parameters
#     )
#
#     sample_size = 10000
#     xx = my_univariate_input.get_sample(sample_size)
#     icdf_values = my_univariate_input.icdf(xx)
#
#     # Assertions
#     # Test the lower bound of sampled ICDF
#     assert np.min(icdf_values) >= my_univariate_input.lower
#     # Test the upper bound of sampled ICDF
#     assert np.max(icdf_values) <= my_univariate_input.upper
#     # Test the lower bound of ICDF
#     assert np.isclose(
#         my_univariate_input.icdf(0.0), my_univariate_input.lower
#     )
#     # Test the upper bound of ICDF
#     assert np.isclose(
#         my_univariate_input.icdf(1.0), my_univariate_input.upper
#     )
#
#
#
