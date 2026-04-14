"""
Test suite for the Parameters class.
"""

import numpy as np
import pytest

from conftest import create_random_alphanumeric
from uqtestfuns.core.parameters import Parameters


@pytest.fixture(params=[1, 2, 3])
def num_params(request):
    return request.param


@pytest.fixture(params=[1, 5, 10])
def dimension(request):
    return request.param


def create_values(num_params):
    values = {}
    descriptions = {}
    for _ in range(num_params):
        key = create_random_alphanumeric(4)
        values[key] = np.random.rand()
        descriptions[key] = create_random_alphanumeric(8)

    return values, descriptions


class TestConstruction:
    """All tests related to the construction of Parameters."""

    def test_default(self, num_params):
        """Test the default construction of Parameters."""
        values, _ = create_values(num_params)

        # Create an instance
        params = Parameters(values)

        # Assertions
        assert len(params) == num_params
        for description in params.descriptions.values():
            assert description is None
        assert params.values == values
        assert params.name is None

    def test_with_name_descriptions(self, num_params):
        """Test the construction of Parameters with name and descriptions."""
        values, descriptions = create_values(num_params)

        # Create an instance
        name = create_random_alphanumeric(4)
        params = Parameters(values, name=name, descriptions=descriptions)

        # Assertions
        assert len(params) == num_params
        assert params.descriptions == descriptions
        assert params.values == values
        assert params.name == name

    def test_with_factory_function(self, dimension):
        """Test the construction of Parameters using a factory function."""

        def factory_function(dimension_: int):
            return np.random.rand(dimension_)

        # Create an instance
        value = {"a": factory_function}
        params = Parameters(value, dimension=dimension)

        # Assertions
        assert len(params) == 1
        assert params["a"].shape == (dimension,)

    def test_with_factory_function_with_kwargs(self, dimension):
        """Test the construction using a factory function with kwargs."""

        def factory_function(dimension_: int, shift_: float = 0.0):
            return shift_ + np.random.rand(dimension_)

        # Create an instance
        value = {"a": factory_function}
        shift = 5.0
        params = Parameters(
            value,
            dimension=dimension,
            factory_kwargs={"a": {"shift_": shift}},
        )

        # Assertions
        assert len(params) == 1
        assert params["a"].shape == (dimension,)
        assert np.unique(np.floor(params["a"])) == shift

    @pytest.mark.parametrize(
        "valid_dimension",
        [1, 2.0, np.array([1])],
    )
    def test_valid_dimension(self, valid_dimension):
        """Test the construction of Parameters with a valid dimension."""

        def factory_function(dimension: int):
            return np.random.rand(dimension)

        # Create an instance
        value = {"a": factory_function}
        params = Parameters(value, dimension=valid_dimension)

        # Assertion
        assert len(params["a"]) == valid_dimension

    def test_with_factory_function_no_dimension(self):
        """Test the construction using a factory function without dimension."""

        def factory_function(dimension_: int):
            return np.random.rand(dimension_)

        # Create an instance
        value = {"a": factory_function}

        with pytest.raises(ValueError):
            _ = Parameters(value)

    @pytest.mark.parametrize(
        "invalid_dimension",
        [1.1, -1, np.array([1, 2]), True, "a"],
    )
    def test_invalid_dimension(self, num_params, invalid_dimension):
        """Test the construction of Parameters with an invalid dimension."""
        values, _ = create_values(num_params)

        # Create an instance
        with pytest.raises(ValueError):
            _ = Parameters(values, dimension=invalid_dimension)

    def test_with_factory_function_invalid_kwargs(self, dimension):
        """Test the construction of Parameters using a factory function."""

        def factory_function(dimension_: int, shift: float = 0.0):
            return shift + np.random.rand(dimension_)

        # Create an instance
        value = {"a": factory_function}

        # Assertion
        with pytest.raises(KeyError):
            _ = Parameters(
                value,
                dimension=dimension,
                factory_kwargs={"b": {"shift": 1.0}},
            )


class TestDescribe:
    """All tests related to the describe() method of Parameters."""

    def test_default(self, num_params):
        """Test the default behavior of describe()."""
        values, descriptions = create_values(num_params)

        # Create an instance
        params = Parameters(values, descriptions=descriptions)

        # Assertions
        for key in params.values.keys():
            assert params.describe(key) == descriptions[key]

    def test_invalid_key(self, num_params):
        """Test the behavior of describe() with an invalid key."""
        values, descriptions = create_values(num_params)

        # Create an instance
        params = Parameters(values, descriptions=descriptions)

        # Assertion
        with pytest.raises(KeyError):
            _ = params.describe("invalid_key")


class TestPrint:
    """All tests related to the print(), repr(), and str() functions."""

    def test_repr(self, num_params):
        """Test __repr__ method of an instance of ProbInput."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, descriptions=descriptions)

        # Create a repr string
        my_repr = repr(params)

        # Assertion
        assert isinstance(my_repr, str)

    def test_str(self, num_params):
        """Test __str__ method of an instance of ProbInput."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, descriptions=descriptions)

        # Create a str string
        my_str = str(params)

        # Assertion
        assert isinstance(my_str, str)

    def test_str_with_name(self, num_params):
        """Test __str__ method of an instance of ProbInput with name."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        name = create_random_alphanumeric(4)
        params = Parameters(values, name=name, descriptions=descriptions)

        # Create a str string
        my_str = str(params)

        # Assertion
        assert isinstance(my_str, str)
        assert name in my_str

    def test_repr_contains_class_name(self, num_params):
        """Test that __repr__ method includes class name."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, descriptions=descriptions)

        # Assertion
        assert f"{Parameters.__name__}(" in repr(params)

    def test_str_without_name_omits_name_line(self, num_params):
        """Test that __str__ omits the name line if no name is provided."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, descriptions=descriptions)

        # Assertion
        assert "Name   :" not in str(params)

    def test_str_various_data_types(self):
        """Test __str__ with various data types for values and descriptions."""
        array_value = np.array([1, 2, 3])
        values = {
            "a": 42,
            "b": "test",
            "c": 1.5,
            "d": array_value,
        }
        params = Parameters(values)

        # Assertion
        assert f"{array_value.shape} array" in str(params)
