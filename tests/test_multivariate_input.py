import pytest
import numpy as np
from tabulate import tabulate

from uqtestfuns.core.prob_input.multivariate_input import MultivariateInput
from conftest import create_random_input_dicts


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_create_instance_numpy_parameters(spatial_dimension):
    """Test the creation of MultivariateInput instance."""
    input_dicts = create_random_input_dicts(spatial_dimension)

    my_multivariate_input = MultivariateInput(input_dicts)

    # Assertions
    # Test the dimensionality
    assert my_multivariate_input.spatial_dimension == spatial_dimension
    for i in range(spatial_dimension):
        # Test the name of the marginals
        assert input_dicts[i]["name"] == my_multivariate_input.marginals[i].name
        # Test the type of distributions
        assert input_dicts[i]["distribution"] == \
               my_multivariate_input.marginals[i].distribution
        # Test the parameter values
        assert np.allclose(
            input_dicts[i]["parameters"],
            my_multivariate_input.marginals[i].parameters
        )


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_generate_sample(spatial_dimension):
    """Test sample generation from an instance of MultivariateInput."""
    input_dicts = create_random_input_dicts(spatial_dimension)

    my_multivariate_input = MultivariateInput(input_dicts)

    sample_size = 5325
    xx = my_multivariate_input.get_sample(sample_size)

    # Assertions
    # Test the number of sample points
    assert xx.shape[0] == sample_size
    # Test the dimensionality of the sample
    assert xx.shape[1] == spatial_dimension
    # Test the bounds
    for i in range(spatial_dimension):
        assert np.min(xx[:, i]) >= my_multivariate_input.marginals[i].lower
        assert np.max(xx[:, i]) <= my_multivariate_input.marginals[i].upper


def test_generate_dependent_sample():
    """Test dependent sample generation (not yet supported)."""
    input_dicts = create_random_input_dicts(5)

    my_multivariate_input = MultivariateInput(input_dicts)
    my_multivariate_input.copulas = []

    with pytest.raises(ValueError) as e_info:
        my_multivariate_input.get_sample(1000)


@pytest.mark.parametrize("spatial_dimension", [1, 5])
def test_get_pdf_values(spatial_dimension):
    """Test the PDF values from an instance of MultivariateInput."""
    input_dicts = create_random_input_dicts(spatial_dimension)

    my_multivariate_input = MultivariateInput(input_dicts)

    sample_size = 100
    xx = my_multivariate_input.get_sample(sample_size)
    pdf_values = my_multivariate_input.pdf(xx)

    # Assert the positiveness of the PDF value
    assert np.all(pdf_values >= 0)
    assert np.all(pdf_values < np.inf)


def test_get_dependent_pdf_values():
    """Test dependent PDF value computation (not yet supported)."""
    input_dicts = create_random_input_dicts(5)

    my_multivariate_input = MultivariateInput(input_dicts)
    my_multivariate_input.copulas = []

    with pytest.raises(ValueError) as e_info:
        my_multivariate_input.pdf(np.random.rand(2, 5))


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10])
def test_transform_sample(spatial_dimension):
    """Test the transformation of sample values from one dist. to another."""
    input_dicts_1 = create_random_input_dicts(spatial_dimension)
    my_multivariate_input_1 = MultivariateInput(input_dicts_1)

    sample_size = 5000
    xx = my_multivariate_input_1.get_sample(sample_size)

    input_dicts_2 = create_random_input_dicts(spatial_dimension)
    my_multivariate_input_2 = MultivariateInput(input_dicts_2)

    xx_trans = my_multivariate_input_1.transform_sample(
        my_multivariate_input_2, xx
    )

    # Assertions
    for i, marginal in enumerate(my_multivariate_input_2.marginals):
        assert np.min(xx_trans[:, i]) >= marginal.lower
        assert np.max(xx_trans[:, i]) <= marginal.upper


def test_failed_transform_sample():
    """Test the failure of sample transformation for MultiVariateInput."""
    input_dicts_1 = create_random_input_dicts(5)
    my_multivariate_input_1 = MultivariateInput(input_dicts_1)

    input_dicts_2 = create_random_input_dicts(10)
    my_multivariate_input_2 = MultivariateInput(input_dicts_2)

    sample_size = 5000
    xx = my_multivariate_input_1.get_sample(sample_size)

    with pytest.raises(ValueError) as e_info:
        my_multivariate_input_1.transform_sample(my_multivariate_input_2, xx)


def test_transform_dependent_sample():
    """Test dependent transformation (not yet supported)."""
    input_dicts_1 = create_random_input_dicts(5)
    my_multivariate_input_1 = MultivariateInput(input_dicts_1)

    input_dicts_2 = create_random_input_dicts(5)
    my_multivariate_input_2 = MultivariateInput(input_dicts_2)

    xx = np.random.rand(2, 5)

    with pytest.raises(ValueError) as e_info:
        my_multivariate_input_1.copulas = []
        my_multivariate_input_1.transform_sample(my_multivariate_input_2, xx)


def test_str():
    """Test __str__ method of an instance of MultivariateInput."""

    # Create a test instance
    input_dicts = create_random_input_dicts(2)
    my_multivariate_input = MultivariateInput(input_dicts)

    # Create the reference string
    header_names = ["name", "distribution", "parameters", "description"]
    str_ref = [
        [i+1] + list(map(input_dict.get, header_names)) for
        i, input_dict in enumerate(input_dicts)
    ]
    header_names.insert(0, "No.")
    str_ref = tabulate(
        str_ref,
        headers=list(map(str.capitalize, header_names)),
        stralign="center"
    )

    # Assertion
    assert my_multivariate_input.__str__() == str_ref


def test_repr_html():
    """Test _repr_html_ method of an instance of MultivariateInput."""

    # Create a test instance
    input_dicts = create_random_input_dicts(5)
    my_multivariate_input = MultivariateInput(input_dicts)

    # Create the reference string
    header_names = ["name", "distribution", "parameters", "description"]
    str_ref = [
        [i+1] + list(map(input_dict.get, header_names)) for
        i, input_dict in enumerate(input_dicts)
    ]
    header_names.insert(0, "No.")
    str_ref = tabulate(
        str_ref,
        headers=list(map(str.capitalize, header_names)),
        stralign="center",
        tablefmt="html"
    )

    # Assertion
    assert my_multivariate_input._repr_html_() == str_ref

#
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
