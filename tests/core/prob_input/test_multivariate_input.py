import pytest
import numpy as np
from tabulate import tabulate
from typing import List, Any

from uqtestfuns.core.prob_input.probabilistic_input import ProbInput
from uqtestfuns.core.prob_input.univariate_distribution import UnivDist
from uqtestfuns.core.prob_input.input_spec import (
    UnivDistSpec,
    ProbInputSpecFixDim,
    ProbInputSpecVarDim,
)
from conftest import create_random_marginals


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_create_instance_numpy_parameters(spatial_dimension):
    """Test the creation of a MultivariateInput instance."""
    marginals = create_random_marginals(spatial_dimension)

    my_multivariate_input = ProbInput(marginals)

    # Assertions
    # Test the dimensionality
    assert my_multivariate_input.spatial_dimension == spatial_dimension
    for i in range(spatial_dimension):
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


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_generate_sample(spatial_dimension):
    """Test sample generation from an instance of MultivariateInput."""
    marginals = create_random_marginals(spatial_dimension)

    my_multivariate_input = ProbInput(marginals)

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
    """Test dependent sample generation (not yet supported; raise error)."""
    marginals = create_random_marginals(5)

    my_multivariate_input = ProbInput(marginals)
    my_multivariate_input.copulas = "a"

    with pytest.raises(ValueError):
        my_multivariate_input.get_sample(1000)


@pytest.mark.parametrize("spatial_dimension", [1, 5])
def test_get_pdf_values(spatial_dimension):
    """Test the PDF values from an instance of MultivariateInput."""
    marginals = create_random_marginals(spatial_dimension)

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

    my_multivariate_input = ProbInput(marginals)
    my_multivariate_input.copulas = "b"

    with pytest.raises(ValueError):
        my_multivariate_input.pdf(np.random.rand(2, 5))


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10])
def test_transform_sample(spatial_dimension):
    """Test the transformation of sample values from one dist. to another."""
    marginals_1 = create_random_marginals(spatial_dimension)
    my_multivariate_input_1 = ProbInput(marginals_1)

    sample_size = 5000
    xx = my_multivariate_input_1.get_sample(sample_size)

    marginals_2 = create_random_marginals(spatial_dimension)
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
    my_multivariate_input_1 = ProbInput(marginals_1)

    marginals_2 = create_random_marginals(5)
    my_multivariate_input_2 = ProbInput(marginals_2)

    xx = np.random.rand(2, 5)

    with pytest.raises(ValueError):
        my_multivariate_input_1.copulas = "a"
        my_multivariate_input_1.transform_sample(xx, my_multivariate_input_2)


def test_str():
    """Test __str__ method of an instance of MultivariateInput."""

    # Create a test instance
    marginals = create_random_marginals(2)
    my_multivariate_input = ProbInput(marginals)

    # Create the reference string
    str_ref = f"Name         : {my_multivariate_input.name}\n"
    str_ref += f"Spatial Dim. : {my_multivariate_input.spatial_dimension}\n"
    str_ref += f"Description  : {my_multivariate_input.description}\n"
    str_ref += "Marginals    :\n\n"
    header_names = ["name", "distribution", "parameters", "description"]
    str_ref_list: List[List] = []
    for i, marginal in enumerate(marginals):
        str_ref_placeholder: List[Any] = [i + 1]
        for header_name in header_names:
            str_ref_placeholder.append(getattr(marginal, header_name))
        str_ref_list.append(str_ref_placeholder)
    header_names.insert(0, "No.")
    str_ref += tabulate(
        str_ref_list,
        headers=list(map(str.capitalize, header_names)),
        stralign="center",
    )
    str_ref += f"\n\nCopulas      : {my_multivariate_input.copulas}"

    # Assertion
    assert my_multivariate_input.__str__() == str_ref


def test_repr_html():
    """Test _repr_html_ method of an instance of MultivariateInput."""

    # Create a test instance
    marginals = create_random_marginals(5)
    my_multivariate_input = ProbInput(marginals)

    # Create the reference string
    str_ref = f"<p><b>Name</b>:&nbsp;{my_multivariate_input.name}\n</p>"
    str_ref += (
        f"<p><b>Spatial Dimension</b>:&nbsp;"
        f"{my_multivariate_input.spatial_dimension}\n</p>"
    )
    str_ref += (
        "<p><b>Description</b>:&nbsp;"
        f"{my_multivariate_input.description}\n</p>"
    )
    str_ref += "<p><b>Marginals:</b>\n</p>"

    header_names = ["name", "distribution", "parameters", "description"]
    str_ref_list: List[List] = []
    for i, marginal in enumerate(marginals):
        str_ref_placeholder: List[Any] = [i + 1]
        for header_name in header_names:
            str_ref_placeholder.append(getattr(marginal, header_name))
        str_ref_list.append(str_ref_placeholder)
    header_names.insert(0, "No.")
    str_ref += tabulate(
        str_ref_list,
        headers=list(map(str.capitalize, header_names)),
        stralign="center",
        tablefmt="html",
    )

    str_ref += "\n"
    str_ref += f"<p><b>Copulas</b>:&nbsp;{my_multivariate_input.copulas}</p>"

    # Assertion
    assert my_multivariate_input._repr_html_() == str_ref


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_pass_random_seed(spatial_dimension):
    """Test passing random seed to the constructor."""
    marginals = create_random_marginals(spatial_dimension)

    # Create two instances with an identical seed number
    rng_seed = 42
    my_input_1 = ProbInput(marginals, rng_seed=rng_seed)
    my_input_2 = ProbInput(marginals, rng_seed=rng_seed)

    # Generate sample points
    xx_1 = my_input_1.get_sample(1000)
    xx_2 = my_input_2.get_sample(1000)

    # Assertion: Both samples are identical because the seed is identical
    assert np.allclose(xx_1, xx_2)


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, 100])
def test_create_from_spec(spatial_dimension):
    """Test creating an instance from specification NamedTuple"""
    marginals: List[UnivDist] = create_random_marginals(spatial_dimension)

    # Create a ProbInputSpecFixDim
    name = "Test Name"
    description = "Test description"
    copulas = None
    prob_spec = ProbInputSpecFixDim(
        name=name,
        description=description,
        marginals=[
            UnivDistSpec(
                name=marginal.name,
                description=marginal.description,
                distribution=marginal.distribution,
                parameters=marginal.parameters,  # type: ignore
            )
            for marginal in marginals
        ],
        copulas=copulas,
    )

    # Create from spec
    my_input = ProbInput.from_spec(prob_spec)

    # Assertions
    assert my_input.name == name
    assert my_input.description == description
    assert my_input.copulas == copulas

    # Create a ProbInputSpecVarDim
    def _test_vardim(spatial_dimension):
        marginals_spec = [
            UnivDistSpec(
                name=f"x{i+1}",
                description="None",
                distribution="uniform",
                parameters=[0, 1],
            )
            for i in range(spatial_dimension)
        ]

        return marginals_spec

    name = "Test Name"
    description = "Test description"
    copulas = None
    prob_spec_vardim = ProbInputSpecVarDim(
        name=name,
        description=description,
        marginals_generator=_test_vardim,
        copulas=copulas,
    )

    # Create from spec
    my_input = ProbInput.from_spec(
        prob_spec_vardim, spatial_dimension=spatial_dimension
    )

    # Assertions
    assert my_input.name == name
    assert my_input.description == description
    assert my_input.copulas == copulas
    assert my_input.spatial_dimension == spatial_dimension

    with pytest.raises(ValueError):
        ProbInput.from_spec(prob_spec_vardim)


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
