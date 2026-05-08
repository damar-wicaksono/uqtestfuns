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
        assert dict(params) == values
        assert params.name is None

    def test_with_name_descriptions(self, num_params):
        """Test the construction of Parameters with name and descriptions."""
        values, descriptions = create_values(num_params)

        # Create an instance
        name = create_random_alphanumeric(4)
        params = Parameters(
            values,
            name=name,
            keyword_descriptions=descriptions,
        )

        # Assertions
        assert len(params) == num_params
        assert dict(params) == values
        assert params.name == name

    def test_empty(self):
        """Test the construction of an empty Parameters instance."""
        params = Parameters({})
        assert len(params) == 0
        assert not params


class TestDescribe:
    """All tests related to the describe() method of Parameters."""

    def test_default(self, num_params):
        """Test the default behavior of describe()."""
        values, descriptions = create_values(num_params)

        # Create an instance
        params = Parameters(values, keyword_descriptions=descriptions)

        # Assertions
        for key in params.keys():
            assert params.describe(key) == descriptions[key]

    def test_invalid_key(self, num_params):
        """Test the behavior of describe() with an invalid key."""
        values, descriptions = create_values(num_params)

        # Create an instance
        params = Parameters(values, keyword_descriptions=descriptions)

        # Assertion
        with pytest.raises(KeyError):
            _ = params.describe("invalid_key")


class TestPrint:
    """All tests related to the print(), repr(), and str() functions."""

    def test_repr(self, num_params):
        """Test __repr__ method of an instance of ProbInput."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, keyword_descriptions=descriptions)

        # Create a repr string
        my_repr = repr(params)

        # Assertion
        assert isinstance(my_repr, str)

    def test_str(self, num_params):
        """Test __str__ method of an instance of ProbInput."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, keyword_descriptions=descriptions)

        # Create a str string
        my_str = str(params)

        # Assertion
        assert isinstance(my_str, str)

    def test_str_with_name(self, num_params):
        """Test __str__ method of an instance of ProbInput with name."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        name = create_random_alphanumeric(4)
        params = Parameters(
            values,
            name=name,
            keyword_descriptions=descriptions,
        )

        # Create a str string
        my_str = str(params)

        # Assertion
        assert isinstance(my_str, str)
        assert name in my_str

    def test_repr_contains_class_name(self, num_params):
        """Test that __repr__ method includes class name."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, keyword_descriptions=descriptions)

        # Assertion
        assert f"{Parameters.__name__}(" in repr(params)

    def test_str_without_name_omits_name_line(self, num_params):
        """Test that __str__ omits the name line if no name is provided."""
        # Create a test instance
        values, descriptions = create_values(num_params)
        params = Parameters(values, keyword_descriptions=descriptions)

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
