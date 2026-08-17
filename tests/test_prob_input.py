import pytest
import numpy as np

from uqtestfuns import Marginal, ProbInput
from conftest import create_random_marginals, create_random_marginal_dicts

# Dimension (`m`)
DIMENSIONS = [1, 2, 10, 100]


def _id_m(dimension):
    return f"m={dimension}"


@pytest.fixture(params=DIMENSIONS, ids=_id_m)
def dimension(request):
    """Return dimension (`m`) fixture."""
    return request.param


class TestConstructor:
    """All tests related to the constructor of ProbInput."""

    def test_default(self, dimension):
        """Test the creation of a ProbInput via the default constructor."""
        marginals = create_random_marginals(dimension)
        test_name = "test_name"

        # Create an instance
        prob_input = ProbInput(marginals, name=test_name)

        # Assertions
        assert prob_input.dimension == dimension
        assert prob_input.name == test_name
        assert prob_input.copulas is None
        for i in range(dimension):
            assert marginals[i] == prob_input.marginals[i]


class TestGetSample:
    """All tests related to the get_sample() method of ProbInput."""

    def test_default(self, dimension):
        """Test the generation of sample point."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate a sample point
        xx = prob_input.get_sample()

        # Assertion
        assert len(xx) == 1
        assert xx.shape[1] == dimension

    def test_rng_reproducible(self, dimension):
        """Test the generation of sample points with a NumPy rng."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 1000
        rng = np.random.default_rng(42)
        xx_1 = prob_input.get_sample(sample_size, rng)
        # Reset the RNG and generate new sample points
        rng = np.random.default_rng(42)
        xx_2 = prob_input.get_sample(sample_size, rng)

        # Assertion
        assert np.allclose(xx_1, xx_2)

    def test_rng_continuing_stream(self, dimension):
        """Test that successive calls with same Generator differ."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 1000
        rng = np.random.default_rng(42)
        xx_1 = prob_input.get_sample(sample_size, rng)
        xx_2 = prob_input.get_sample(sample_size, rng)

        # Assertion
        assert not np.allclose(xx_1, xx_2)

    def test_rng_int(self, dimension):
        """Test the generation of sample points with an integer seed."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 1000
        rng = 42
        xx_1 = prob_input.get_sample(sample_size, rng)
        xx_2 = prob_input.get_sample(sample_size, rng)

        # Assertion
        assert np.allclose(xx_1, xx_2)

    def test_get_sample(self, dimension):
        """Test sample generation of a given size."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 5325
        xx = prob_input.get_sample(sample_size)

        # Assertions
        # Test the number of sample points
        assert xx.shape[0] == sample_size
        # Test the dimensionality of the sample
        assert xx.shape[1] == dimension
        # Test the bounds
        for i in range(dimension):
            assert np.min(xx[:, i]) >= prob_input.marginals[i].lower
            assert np.max(xx[:, i]) <= prob_input.marginals[i].upper

    def test_generate_dependent_sample(self, dimension):
        """Test dependent sample generation (unsupported; raise error)."""
        marginals = create_random_marginals(dimension)

        my_multivariate_input = ProbInput(marginals, "a")

        with pytest.raises(ValueError):
            my_multivariate_input.get_sample(1000)


class TestPDF:
    """All tests related to the pdf() method of ProbInput."""

    def test_default(self, dimension):
        """Test the PDF computation for a given input."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 100
        xx = prob_input.get_sample(sample_size)

        # Compute the PDF values
        pdf_values = prob_input.pdf(xx)

        # Assertions
        assert len(pdf_values) == sample_size
        assert pdf_values.ndim == 1
        assert np.all(pdf_values >= 0)
        assert np.all(pdf_values < np.inf)

    def test_single_value(self, dimension):
        """Test the PDF computation for a single input value."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate a sample point
        sample_size = 1
        xx = prob_input.get_sample(sample_size)[0, :]

        # Compute the PDF values
        pdf_values = prob_input.pdf(xx)

        # Assertions
        assert len(pdf_values) == sample_size
        assert pdf_values.ndim == 1
        assert np.all(pdf_values >= 0)
        assert np.all(pdf_values < np.inf)

    def test_get_dependent_pdf_values(self, dimension):
        """Test dependent PDF value computation (not yet supported)."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals, copulas="b")

        with pytest.raises(ValueError):
            _ = prob_input.pdf(np.random.rand(2, dimension))

    def test_invalid_input(self, dimension):
        """Test invalid input for the pdf() method."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate a sample point
        xx = np.random.rand(100, dimension + 1)

        # Compute the PDF values
        with pytest.raises(ValueError):
            _ = prob_input.pdf(xx)

    def test_known_value(self):
        """Test PDF against known analytical value."""
        # Create an instance
        prob_input = ProbInput(
            [
                Marginal(distribution="uniform", parameters=[0.0, 2.0]),
                Marginal(distribution="uniform", parameters=[0.0, 5.0]),
            ]
        )

        # Generate sample points
        xx = prob_input.get_sample(1000)

        # Assertion: Joint PDF = 1/2 * 1/5 = 0.1
        assert np.allclose(prob_input.pdf(xx), 0.1)


class TestCDF:
    """All tests related to the cdf() method of ProbInput."""

    def test_default(self, dimension):
        """Test the CDF computation for a given input."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 100
        xx = prob_input.get_sample(sample_size)

        # Compute the CDF values
        cdf_values = prob_input.cdf(xx)

        # Assertions
        assert len(cdf_values) == sample_size
        assert cdf_values.ndim == 1
        assert np.all(cdf_values >= 0.0)
        assert np.all(cdf_values <= 1.0)

    def test_single_value(self, dimension):
        """Test the CDF computation for a single input value."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate a sample point
        sample_size = 1
        xx = prob_input.get_sample(sample_size)[0, :]

        # Compute the CDF values
        cdf_values = prob_input.cdf(xx)

        # Assertions
        assert len(cdf_values) == sample_size
        assert cdf_values.ndim == 1
        assert np.all(cdf_values >= 0.0)
        assert np.all(cdf_values <= 1.0)

    def test_get_dependent_cdf_values(self, dimension):
        """Test dependent CDF value computation (not yet supported)."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals, copulas="b")

        with pytest.raises(ValueError):
            _ = prob_input.cdf(np.random.rand(2, dimension))

    def test_invalid_input(self, dimension):
        """Test invalid input for the cdf() method."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate a sample point
        xx = np.random.rand(100, dimension + 1)

        # Compute the PDF values
        with pytest.raises(ValueError):
            _ = prob_input.cdf(xx)

    def test_known_value(self):
        """Test PDF against known analytical value."""
        # Create an instance
        prob_input = ProbInput(
            [
                Marginal(distribution="uniform", parameters=[0.0, 2.0]),
                Marginal(distribution="uniform", parameters=[0.0, 5.0]),
            ]
        )

        # Generate sample points
        xx = np.array(
            [
                [0.0, 0.0],  # 0.0 * 0.0 = 0.0
                [2.0, 0.0],  # 0.0 * 0.0 = 0.0
                [0.0, 5.0],  # 0.0 * 0.0 = 0.0
                [2.0, 5.0],  # 1.0 * 1.0 = 1.0
                [1.0, 2.5],  # 0.5 * 0.5 = 0.25
            ]
        )

        # Assertion
        cdf_ref = np.array([0.0, 0.0, 0.0, 1.0, 0.25])
        assert np.allclose(prob_input.cdf(xx), cdf_ref)


class TestTransformation:
    """All tests related to the transformation methods of ProbInput."""

    def test_transform_to(self, dimension):
        """Test the transformation of sample values to another distribution."""
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1)

        marginals_2 = create_random_marginals(dimension)
        prob_input_2 = ProbInput(marginals_2)

        # Generate sample
        sample_size = 5000
        xx_1 = prob_input_1.get_sample(sample_size)

        # Transform the sample points
        xx_2 = prob_input_1.transform_to(xx_1, prob_input_2)

        # Assertions
        assert np.allclose(xx_1, prob_input_2.transform_to(xx_2, prob_input_1))
        for i, marginal in enumerate(prob_input_2.marginals):
            assert np.min(xx_2[:, i]) >= marginal.lower
            assert np.max(xx_2[:, i]) <= marginal.upper

    def test_transform_from(self, dimension):
        """Test the transformation of sample from another distribution."""
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1)

        marginals_2 = create_random_marginals(dimension)
        prob_input_2 = ProbInput(marginals_2)

        # Generate sample
        sample_size = 5000
        xx_2 = prob_input_2.get_sample(sample_size)

        # Transform the sample points
        xx_1 = prob_input_1.transform_from(xx_2, prob_input_2)
        xx_2_ = prob_input_2.transform_from(xx_1, prob_input_1)

        # Assertions
        assert np.allclose(xx_2, xx_2_)
        for i, marginal in enumerate(prob_input_1.marginals):
            assert np.min(xx_1[:, i]) >= marginal.lower
            assert np.max(xx_1[:, i]) <= marginal.upper

    def test_failed_transform_sample(self, dimension):
        """Test the failure of sample transformation."""
        marginals_1 = create_random_marginals(dimension)
        my_multivariate_input_1 = ProbInput(marginals_1)

        marginals_2 = create_random_marginals(dimension + 1)
        my_multivariate_input_2 = ProbInput(marginals_2)

        sample_size = 5000
        xx = my_multivariate_input_1.get_sample(sample_size)

        # Transformation between two random variables of different dimensions
        with pytest.raises(ValueError):
            my_multivariate_input_1.transform_to(xx, my_multivariate_input_2)
        with pytest.raises(ValueError):
            my_multivariate_input_1.transform_from(xx, my_multivariate_input_2)

    def test_transform_dependent_sample(self, dimension):
        """Test dependent transformation (unsupported; raise an error)."""
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1, copulas="a")

        marginals_2 = create_random_marginals(dimension)
        prob_input_2 = ProbInput(marginals_2, copulas="b")

        xx = np.random.rand(2, dimension)

        # Assertions
        with pytest.raises(ValueError):
            _ = prob_input_1.transform_to(xx, prob_input_2)

        with pytest.raises(ValueError):
            _ = prob_input_2.transform_to(xx, prob_input_1)

    def test_transform_to_hypercube(self, dimension):
        """Test the transformation of sample values to a hypercube."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Generate sample
        sample_size = 5000
        xx = prob_input.get_sample(sample_size)

        # Transform to hypercube
        xx_trans = prob_input.transform_to(xx)

        # Assertions
        assert np.all(xx_trans >= -1.0)
        assert np.all(xx_trans <= 1.0)

    def test_transform_from_hypercube(self, dimension):
        """Test the transformation of sample values from a hypercube."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Generate sample
        sample_size = 5000
        rng = np.random.default_rng(42)
        xx = rng.random((sample_size, dimension))

        # Transform from hypercube
        xx_trans = prob_input.transform_from(xx, (0.0, 1.0))

        # Assertions
        for i, marginal in enumerate(prob_input.marginals):
            assert np.all(xx_trans[:, i] >= marginal.lower)
            assert np.all(xx_trans[:, i] <= marginal.upper)

    def test_round_trip(self, dimension):
        """Test the round-trip transformation of sample values."""
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Generate sample
        sample_size = 5000
        xx_1 = prob_input.get_sample(sample_size)

        # Transform the sample points
        xx_2 = prob_input.transform_to(xx_1)
        xx_1_ = prob_input.transform_from(xx_2)

        # Assertion
        assert np.allclose(xx_1, xx_1_)

    def test_transform_to_from(self, dimension):
        """Test that transformation to and from are inverses."""
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1)

        marginals_2 = create_random_marginals(dimension)
        prob_input_2 = ProbInput(marginals_2)

        # Generate sample
        sample_size = 5000
        xx_1 = prob_input_1.get_sample(sample_size)

        # Transform the sample points
        xx_2_a = prob_input_1.transform_from(xx_1, prob_input_2)
        xx_2_b = prob_input_2.transform_to(xx_1, prob_input_1)

        # Assertion
        assert np.allclose(xx_2_a, xx_2_b)


class TestEquality:
    """All tests related to the equality operator."""

    def test_equal(self, dimension):
        """Test equality operator for ProbInput instances."""
        marginal_dicts = create_random_marginal_dicts(dimension)
        marginals = [
            Marginal(**marginal_dict) for marginal_dict in marginal_dicts
        ]

        # Create instances
        prob_input_1 = ProbInput(marginals)
        prob_input_2 = ProbInput(marginals)

        # Assertions
        assert prob_input_1 is not prob_input_2
        assert prob_input_1 == prob_input_2

    @pytest.mark.parametrize("other", [None, 42, "string", [1, 2, 3]])
    def test_not_equal_other_types(self, dimension, other):
        """Test inequality operator for instances with other types."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Assertion
        assert prob_input != other

    def test_not_equal_different_name(self, dimension):
        """Test inequality operator for instances with different names."""
        marginals = create_random_marginals(dimension)

        # Create instances
        prob_input_1 = ProbInput(marginals, name="a")
        prob_input_2 = ProbInput(marginals, name="b")

        # Assertion
        assert prob_input_1 != prob_input_2

    def test_not_equal_copulas(self, dimension):
        """Test inequality operator for instances with different copulas."""
        marginals = create_random_marginals(dimension)

        # Create instances
        prob_input_1 = ProbInput(marginals, copulas="a")
        prob_input_2 = ProbInput(marginals, copulas="b")

        # Assertion
        assert prob_input_1 != prob_input_2

    def test_not_equal_different_dimension(self, dimension):
        """Test inequality operator for instances with different dimensions."""
        # Create instances
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1)
        marginals_2 = create_random_marginals(dimension + 1)
        prob_input_2 = ProbInput(marginals_2)

        # Assertion
        assert prob_input_1 != prob_input_2

    def test_not_equal_different_marginals(self, dimension):
        """Test inequality operator for instances with different marginals."""
        # Create instances
        marginals_1 = create_random_marginals(dimension)
        prob_input_1 = ProbInput(marginals_1)
        marginals_2 = create_random_marginals(dimension)
        prob_input_2 = ProbInput(marginals_2)

        # Assertion
        assert prob_input_1 != prob_input_2


class TestPrint:
    """All tests related to the print(), repr(), and str() functions."""

    def test_repr(self, dimension):
        """Test __repr__ method of an instance of ProbInput."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Create a repr string
        my_str = repr(prob_input)

        # Assertion
        assert isinstance(my_str, str)

    def test_str(self, dimension):
        """Test __str__ method of an instance of ProbInput."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Create a str string
        my_str = str(prob_input)

        # Assertion
        assert isinstance(my_str, str)

    def test_str_with_name(self, dimension):
        """Test __str__ method of an instance of ProbInput."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals, name="Test")

        # Create a str string
        my_str = str(prob_input)

        # Assertion
        assert isinstance(my_str, str)

    def test_repr_contains_class_name(self, dimension):
        """Test that __repr__ method includes class name."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Assertion
        assert "ProbInput(" in repr(prob_input)

    def test_str_contains_dimension(self, dimension):
        """Test that __str__ method includes dimension."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Assertion
        assert str(dimension) in str(prob_input)

    def test_str_with_name_contains_name(self, dimension):
        """Test that __str__ method includes name."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals, name="Test")

        # Assertion
        assert "Test" in str(prob_input)

    def test_str_without_name_omits_name_line(self, dimension):
        """Test that __str__ method omits name line if no name is provided."""
        # Create a test instance
        marginals = create_random_marginals(dimension)
        prob_input = ProbInput(marginals)

        # Assertion
        assert "Name      :" not in str(prob_input)

    def test_str_no_marginal_description(self, dimension):
        """Test __str__ method when the marginals have no description."""
        # Create a test instance
        marginals = []
        for i in range(dimension):
            marginals.append(
                Marginal(
                    name=f"X{i+1}",
                    distribution="uniform",
                    parameters=[0.0, 1.0],
                )
            )
        prob_input = ProbInput(marginals)

        # Assertion
        assert "Description" not in str(prob_input)


class TestValidation:
    """All tests related to array validation."""

    def test_valid_shape(self, dimension):
        """Test a valid shape."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 100
        xx = prob_input.get_sample(sample_size)

        # Assertion
        assert prob_input.is_valid_shape(xx)

    def test_invalid_shape(self, dimension):
        """Test an invalid shape."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points of higher dimension
        sample_size = 100
        rng = np.random.default_rng()
        xx = rng.random((sample_size, prob_input.dimension + 1))

        # Assertion
        assert not prob_input.is_valid_shape(xx)

    def test_valid_domain(self, dimension):
        """Test an array of valid domain."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Generate sample points
        sample_size = 100
        xx = prob_input.get_sample(sample_size)

        # Assertions
        assert prob_input.is_valid_shape(xx)
        assert np.all(prob_input.is_valid_domain(xx))

    def test_invalid_domain(self, dimension):
        """Test an array of invalid domain."""
        marginals = create_random_marginals(dimension)

        # Create an instance
        prob_input = ProbInput(marginals)

        # Array of an invalid domain
        sample_size = 100
        xx = np.full((sample_size, prob_input.dimension), np.inf)

        # Assertions
        assert prob_input.is_valid_shape(xx)
        assert not np.any(prob_input.is_valid_domain(xx))
