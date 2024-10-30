"""
Test module for FunParams class.
"""

import numpy as np
import pytest
import random
import string

from uqtestfuns.core import FunParams


@pytest.fixture
def declared_parameter():
    return {
        "keyword": "param",
        "value": 10,
        "type": int,
        "description": "my parameter",
    }


@pytest.fixture
def declared_parameter_invalid():
    return {
        "keyword": "01param",
        "value": 10,
    }


@pytest.fixture
def declared_parameters():
    return [
        {
            "keyword": "param1",
            "value": 10,
            "type": int,
            "description": "my parameter",
        },
        {
            "keyword": "param2",
            "value": 30.0,
        },
        {
            "keyword": "param3",
            "value": np.random.rand(10, 3),
        },
    ]


@pytest.fixture
def input_dict():
    return {
        "function_id": "test-function",
        "parameter_id": "param-01",
        "description": "my parameter",
        "declared_parameters": [
            {
                "keyword": "param_01",
                "value": 10,
                "type": int,
                "description": "my parameter",
            },
            {
                "keyword": "param_02",
                "value": 20.0,
            },
        ],
    }


def test_bool_true(declared_parameter):
    """Test the boolean value of an instance (True)."""
    my_params = FunParams(declared_parameters=[declared_parameter])

    assert my_params


def test_bool_false():
    """Test the boolean value of an instance (False)."""
    my_params = FunParams()

    assert not my_params


def test_len(declared_parameters):
    """Test the length of an instance."""
    my_params = FunParams(declared_parameters=declared_parameters)

    assert len(my_params) == len(declared_parameters)


class TestEquality:
    """Series of tests for equality check."""

    def test_equal_empty(self):
        """Test the equality in value of two empty instances."""
        my_params_1 = FunParams()
        my_params_2 = FunParams()

        assert my_params_1 == my_params_2

    def test_equal(self, input_dict):
        """Test the equality in value of two instances."""
        my_params_1 = FunParams(**input_dict)
        my_params_2 = FunParams(**input_dict)

        assert my_params_1 == my_params_2

    @pytest.mark.parametrize("other", [1, [1, 2], np.array([1])])
    def test_other_instance(self, other):
        """Test the equality check with other instances."""
        my_params = FunParams()

        assert my_params != other

    def test_not_equal(self, declared_parameters):
        """Test the inequality in value of two instances."""
        my_params_1 = FunParams(declared_parameters=declared_parameters)
        my_params_2 = FunParams(declared_parameters=declared_parameters[:-1])

        assert my_params_1 != my_params_2

    def test_equal_array_valued(self):
        """Test the equality of two instances with array-valued parameter."""
        my_params_1 = FunParams()
        my_params_2 = FunParams()
        xx = np.random.rand(10, 10)
        my_params_1.add("xx", xx)
        my_params_2.add("xx", xx)

        assert my_params_1 == my_params_2

    def test_inequal_array_valued(self):
        """Test the inequality of two instances with array-valued parameter."""
        my_params_1 = FunParams()
        my_params_2 = FunParams()
        my_params_1.add("xx", np.random.rand(10, 10))
        my_params_2.add("xx", np.random.rand(5, 3))

        assert my_params_1 != my_params_2


class TestPrint:
    """Series of tests related to print() on the instance."""

    def test_print(self, input_dict):
        """Test that print can be called on an instance."""
        my_params = FunParams(**input_dict)

        out = my_params.__str__()

        assert isinstance(out, str)

    def test_print_empty(self):
        """Test that print can be called on an empty instance."""
        my_params = FunParams()

        out = my_params.__str__()

        assert out == str(None)

    def test_print_long_description(self, declared_parameter):
        """Test print on an instance with long description."""
        my_params = FunParams(
            description=_random_string(150),
            declared_parameters=[declared_parameter],
        )

        out = my_params.__str__()

        assert isinstance(out, str)

    def test_print_arbitrary(self):
        """Test printing instance with arbitrary parameter value."""
        # Create an instance
        my_params = FunParams()
        my_params.add(keyword="param", value=[120, 30])

        out = my_params.__str__()

        assert isinstance(out, str)

    def test_print_array(self):
        """Test printing instance with array parameter value."""
        # Create an instance
        my_params = FunParams()
        my_params.add(keyword="param", value=np.random.rand(10, 3))

        out = my_params.__str__()

        assert isinstance(out, str)


class TestAddParameter:
    """Series of tests for adding parameters."""

    def test_full(self, declared_parameter):
        """Test that adding parameters with full parameter specification."""
        # Create an empty instance
        my_params = FunParams()

        # Add parameter
        my_params.add(**declared_parameter)

        # Assertion
        assert len(my_params) == 1

    def test_repeated(self, declared_parameter):
        """Test that adding parameter multiple times raises an exception."""
        # Create an empty instance
        my_params = FunParams()

        # Add parameter
        my_params.add(**declared_parameter)

        # Assertion
        with pytest.raises(KeyError):
            my_params.add(**declared_parameter)

    def test_invalid_keyword(self, declared_parameter_invalid):
        """Test that adding a parameter w/ invalid keyword raises an exception.

        Notes
        -----
        - A keyword must be a valid Python identifier.
        """
        # Create an empty instance
        my_params = FunParams()

        # Assertion
        with pytest.raises(ValueError):
            my_params.add(**declared_parameter_invalid)

    def test_invalid_type(self):
        """Test that adding a parameter must be consistent with the type."""
        # Create an empty instance
        my_params = FunParams()

        # Assertion
        with pytest.raises(TypeError):
            my_params.add(keyword="param", value="10", type=float)


class TestAssignParameter:
    """Series of tests for assigning parameters after creation."""

    def test_no_type(self):
        """Test assigning a parameter with no type."""
        # Create an instance
        my_params = FunParams()
        my_params.add(keyword="param", value=20)

        assert my_params["param"] == 20

        # Modify the value
        my_params["param"] = "20"

        assert my_params["param"] == "20"

    def test_with_type(self):
        """Test assigning a parameter with provided type."""
        # Create an instance
        my_params = FunParams()
        my_params.add(keyword="param", value=20, type=int)

        assert my_params["param"] == 20

        # Modify the value
        my_params["param"] = 30

        assert my_params["param"] == 30

    def test_invalid_type(self):
        """Test assigning a parameter inconsistent with type"""
        # Create an instance
        my_params = FunParams()
        my_params.add(keyword="param", value=20, type=int)

        assert my_params["param"] == 20

        with pytest.warns(UserWarning):
            my_params["param"] = 20.0

    def test_undeclared(self):
        """Test assigning undeclared parameter."""
        # Create an empty instance
        my_params = FunParams()

        # Assertion
        with pytest.raises(KeyError):
            my_params["param"] = 10


def test_reset_value():
    """Test resetting the value of an instance."""
    # Create an instance
    my_params = FunParams()
    my_params.add(keyword="param", value=10)

    # Change the value
    my_params["param"] = 20

    assert my_params["param"] != 10

    my_params.reset_value()

    assert my_params["param"] == 10


def test_as_dict(declared_parameter):
    """Test as dictionary method."""
    my_params = FunParams()
    my_params.add(**declared_parameter)

    my_params_dict = my_params.as_dict()

    key = declared_parameter["keyword"]
    assert my_params_dict[key] == declared_parameter["value"]


def _random_string(length):
    """Create a random string of a given length."""
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for _ in range(length))

    return result_str
