"""
Test module for RealVariable class.
"""

import numpy as np
import pytest
import random

from uqtestfuns import RealVariable


@pytest.fixture
def realvar_fixture():
    # Generate the bounds randomly
    lower = random.uniform(1.0, 100.0)
    upper = random.uniform(lower, 100.0)

    # Create an instance
    my_realvar = RealVariable(lower, upper)

    return my_realvar


class TestInit:
    """Collection of tests for initialization."""

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_init(self, lower, upper):
        """Test default construction."""
        my_realvar = RealVariable(lower, upper)

        lb, ub = my_realvar.bounds
        assert lb == lower
        assert ub == upper

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    @pytest.mark.parametrize("name_desc", ["a", "b", "c"])
    def test_init_with_name_and_description(self, lower, upper, name_desc):
        """Test construction with specified name and description."""
        my_realvar = RealVariable(lower, upper, name_desc, name_desc)

        lb, ub = my_realvar.bounds
        assert lb == lower
        assert ub == upper

        assert my_realvar.name == name_desc
        assert my_realvar.description == name_desc

    @pytest.mark.parametrize("lower", [5.0, 6.0, 7.0])
    @pytest.mark.parametrize("upper", [4.0, 3.0, 5.0])
    def test_init_invalid_bounds(self, lower, upper):
        """Test construction with invalid bounds."""

        with pytest.raises(ValueError):
            _ = RealVariable(lower, upper)

    def test_type(self, realvar_fixture):
        """Test the types of lower and upper bounds."""
        lower, upper = realvar_fixture.bounds
        assert isinstance(realvar_fixture.bounds, tuple)
        assert isinstance(lower, float)
        assert isinstance(upper, float)

    def test_rng(self, realvar_fixture):
        """Test rng property."""
        # First call, an RNG is created
        rng_1 = realvar_fixture.rng
        assert isinstance(rng_1, np.random.Generator)

        # Second call, the cached RNG is accessed
        rng_2 = realvar_fixture.rng
        assert rng_1 is rng_2


class TestIsValid:
    """Collection of tests for is_valid() method."""

    def test_is_valid_scalar(self, realvar_fixture):
        """Test checking validity of a scalar."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds

        # Generate a random value from within the bound
        val = random.uniform(lower, upper)

        # Assertion
        assert realvar_fixture.is_valid(val)

    def test_is_valid_array(self, realvar_fixture):
        """Test checking the validity of values in an array."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds

        # Generate an array of random values from within the bound
        vals = np.random.uniform(lower, upper, (10,))

        # Assertion
        assert np.all(realvar_fixture.is_valid(vals))

        # Generate an array of random values from within the bound
        vals = np.random.uniform(lower, upper, (10, 10))

        # Assertion
        assert np.all(realvar_fixture.is_valid(vals))

    def test_boundary_scalar(self, realvar_fixture):
        """Test checking the validity of boundary values given as a scalar."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds

        # Assertions
        assert realvar_fixture.is_valid(lower)
        assert realvar_fixture.is_valid(upper)

    def test_boundary_array(self, realvar_fixture):
        """Test checking the validity of boundary values given as an array."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds
        lower = np.ones(10) * lower
        upper = np.ones(10) * upper

        # Assertions
        assert np.all(realvar_fixture.is_valid(lower))
        assert np.all(realvar_fixture.is_valid(upper))

    def test_invalid_bounds(self, realvar_fixture):
        """Test checking the validity of invalid values given as a scalar."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds

        # Assertions
        assert not realvar_fixture.is_valid(lower - 1)
        assert not realvar_fixture.is_valid(upper + 1)

    def test_invalid_array(self, realvar_fixture):
        """Test checking the validity of invalid values given as an array."""
        # Get the bounds
        lower, upper = realvar_fixture.bounds

        # Create arrays with out of bound values
        lower = np.random.uniform(lower - 2, lower - 1, size=(100,))
        upper = np.random.uniform(upper + 1, upper + 2, size=(100,))

        # Assertions
        assert not np.all(realvar_fixture.is_valid(lower))
        assert not np.all(realvar_fixture.is_valid(upper))

    def test_inf_validity(self, realvar_fixture):
        """Test checking the validity of infinity value."""
        assert not realvar_fixture.is_valid(np.inf)
        assert not realvar_fixture.is_valid(-np.inf)

    def test_nan_validity(self, realvar_fixture):
        """Test checking the validity of nan value."""
        assert not realvar_fixture.is_valid(np.nan)


class TestGetSample:
    """Collection of tests for get_sample() method."""

    @pytest.mark.parametrize("sample_size", [1, 10, 100, 1000])
    def test_sample_size(self, realvar_fixture, sample_size):
        """Test generating different sample sizes."""
        xx = realvar_fixture.get_sample(sample_size)

        # Assertion
        assert len(xx) == sample_size

    @pytest.mark.parametrize("sample_size", [1, 10, 100, 1000])
    def test_sample_validity(self, realvar_fixture, sample_size):
        """Test checking the validity of generated samples."""
        xx = realvar_fixture.get_sample(sample_size)

        # Assertions
        assert np.all(realvar_fixture.is_valid(xx))

    @pytest.mark.parametrize("rng_seed", [0, 42, 100])
    def test_reproducibility(self, rng_seed):
        """Test reproducibility of the generated samples."""
        realvar_1 = RealVariable(10, 20, rng_seed=rng_seed)
        realvar_2 = RealVariable(10, 20, rng_seed=rng_seed)

        xx_1 = realvar_1.get_sample(100)
        xx_2 = realvar_2.get_sample(100)

        # Assertions
        assert np.all(xx_1 == xx_2)

    @pytest.mark.parametrize("sample_size", [np.inf, np.nan])
    def test_invalid_sample_size_type(self, realvar_fixture, sample_size):
        """Test the failure of generating samples with invalid size type."""
        with pytest.raises(TypeError):
            _ = realvar_fixture.get_sample(sample_size)

    def test_invalid_sample_size_value(self, realvar_fixture):
        """Test the failure of generating samples with invalid size value."""
        with pytest.raises(ValueError):
            _ = realvar_fixture.get_sample(-1)

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_different_seeds(self, lower, upper):
        """Test initialization with different seeds."""
        realvar_1 = RealVariable(lower, upper, rng_seed=0)
        realvar_2 = RealVariable(lower, upper, rng_seed=1)

        xx_1 = realvar_1.get_sample(100)
        xx_2 = realvar_2.get_sample(100)

        # Assertion
        assert not np.all(xx_1 == xx_2)


class TestTransformTo:
    """Collection of tests for the transform_to() method."""

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_transform_to_scalar(self, realvar_fixture, lower, upper):
        """Test the transformation of a scalar value."""
        realvar_1 = realvar_fixture
        realvar_2 = RealVariable(lower, upper)

        xx_ori = np.random.uniform(*realvar_1.bounds)
        xx_tra = realvar_1.transform_to(xx_ori, lower, upper)

        # Assertion
        assert not np.all(realvar_2.is_valid(xx_ori))
        assert np.all(realvar_2.is_valid(xx_tra))

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_transform_to_array(self, realvar_fixture, lower, upper):
        """Test the transformation of an array of values."""
        realvar_1 = realvar_fixture
        realvar_2 = RealVariable(lower, upper)

        xx_ori = realvar_1.get_sample(100)
        xx_tra = realvar_1.transform_to(xx_ori, lower, upper)

        # Assertion
        assert not np.all(realvar_2.is_valid(xx_ori))
        assert np.all(realvar_2.is_valid(xx_tra))

    @pytest.mark.parametrize("lower", [5.0, 6.0, 7.0])
    @pytest.mark.parametrize("upper", [4.0, 3.0, 5.0])
    def test_invalid_bounds(self, realvar_fixture, lower, upper):
        """Test transformation with invalid bounds."""
        xx_ori = realvar_fixture.get_sample(100)

        with pytest.raises(ValueError):
            _ = realvar_fixture.transform_to(xx_ori, lower, upper)

    def test_invalid_sample(self, realvar_fixture):
        """Test the failure of transformation with an invalid sample."""
        lower_ori, upper_ori = realvar_fixture.bounds
        xx_ori = np.random.uniform(lower_ori - 2, lower_ori - 1, size=(100,))

        with pytest.raises(ValueError):
            # Inconsistent bounds
            _ = realvar_fixture.transform_to(xx_ori, lower_ori, upper_ori)

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_back_and_forth(self, realvar_fixture, lower, upper):
        """Test the back and forth transformation."""
        xx_origin = realvar_fixture.get_sample(100)
        xx_target = realvar_fixture.transform_to(xx_origin, lower, upper)
        xx_origin_2 = realvar_fixture.transform_from(xx_target, lower, upper)

        # Assertions
        assert np.all(realvar_fixture.is_valid(xx_origin_2))
        assert np.allclose(xx_origin, xx_origin_2)


class TestTransformFrom:
    """Collection of tests for the transform_from() method."""

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_transform_from_scalar(self, realvar_fixture, lower, upper):
        """Test the transformation of a scalar value."""
        realvar_1 = realvar_fixture
        realvar_2 = RealVariable(lower, upper)

        xx_ori = np.random.uniform(*realvar_1.bounds)
        xx_tra = realvar_2.transform_from(xx_ori, *realvar_1.bounds)

        # Assertion
        assert not np.all(realvar_2.is_valid(xx_ori))
        assert np.all(realvar_2.is_valid(xx_tra))

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_transform_from_array(self, realvar_fixture, lower, upper):
        """Test the transformation of an array of values."""
        realvar_1 = realvar_fixture
        realvar_2 = RealVariable(lower, upper)

        xx_ori = realvar_1.get_sample(100)
        xx_tra = realvar_2.transform_from(xx_ori, *realvar_1.bounds)

        # Assertion
        assert not np.all(realvar_2.is_valid(xx_ori))
        assert np.all(realvar_2.is_valid(xx_tra))

    @pytest.mark.parametrize("lower", [5.0, 6.0, 7.0])
    @pytest.mark.parametrize("upper", [4.0, 3.0, 5.0])
    def test_invalid_bounds(self, realvar_fixture, lower, upper):
        """Test transformation with invalid bounds."""
        xx_target = realvar_fixture.get_sample(100)

        with pytest.raises(ValueError):
            _ = realvar_fixture.transform_from(xx_target, lower, upper)

    def test_invalid_sample(self, realvar_fixture):
        """Test the failure of transformation with an invalid sample."""
        lower_target, upper_target = realvar_fixture.bounds
        xx_target = np.random.uniform(
            lower_target - 2,
            lower_target - 1,
            size=(100,),
        )

        with pytest.raises(ValueError):
            # Inconsistent bounds
            _ = realvar_fixture.transform_from(
                xx_target,
                lower_target,
                upper_target,
            )

    @pytest.mark.parametrize("lower", [0.0, 1.0, 2.0])
    @pytest.mark.parametrize("upper", [3.0, 4.0, 5.0])
    def test_back_and_forth(self, realvar_fixture, lower, upper):
        """Test the back and forth transformation."""
        realvar_1 = realvar_fixture
        realvar_2 = RealVariable(lower, upper)

        # Create a target sample
        xx_target_1 = realvar_2.get_sample(100)
        xx_origin = realvar_1.transform_from(xx_target_1, lower, upper)
        xx_target_2 = realvar_1.transform_to(xx_origin, lower, upper)

        # Assertions
        assert np.all(realvar_2.is_valid(xx_target_2))
        assert np.allclose(xx_target_1, xx_target_2)


def test_repr(realvar_fixture):
    """Test __repr__ method of an instance."""
    # Create a string
    my_repr = repr(realvar_fixture)

    # Assertion
    assert isinstance(my_repr, str)


def test_str(realvar_fixture):
    """Test __str__ method of an instance."""
    # Create a string
    my_str = str(realvar_fixture)

    # Assertion
    assert isinstance(my_str, str)


@pytest.mark.parametrize("name_desc", ["a", "b", "c"])
def test_str_with_name_and_description(realvar_fixture, name_desc):
    """Test construction with specified name and description."""
    # Create a string
    realvar_fixture.name = name_desc
    realvar_fixture.description = name_desc
    my_str = str(realvar_fixture)

    # Assertion
    assert isinstance(my_str, str)


@pytest.mark.parametrize("rng_seed", [0, 1, 2, 3])
def test_reset_rng(realvar_fixture, rng_seed):
    """Test resetting the RNG of an instance."""
    realvar_fixture.reset_rng(rng_seed)
    xx_1 = realvar_fixture.get_sample(100)

    realvar_fixture.rng_seed = rng_seed
    xx_2 = realvar_fixture.get_sample(100)

    assert np.all(xx_1 == xx_2)
    assert realvar_fixture.rng_seed == rng_seed
