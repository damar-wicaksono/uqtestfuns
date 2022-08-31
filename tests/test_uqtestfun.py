import numpy as np
import pytest
from inspect import signature

from uqtestfuns import UQTestFun, MultivariateInput, get_default_args
from conftest import (
    assert_call, create_random_input_dicts, create_random_alphanumeric
)


@pytest.fixture
def uqtestfun():
    """Create an instance of UQTestFun."""
    input_dicts = create_random_input_dicts(1)

    my_args = {
        "name": "Test function",
        "evaluate": lambda x, p: x + 1,
        "input": MultivariateInput(input_dicts),
        "parameters": 10
    }

    return UQTestFun(**my_args), my_args


def test_create_instance(uqtestfun):
    """Test the creation of an instance of UQTestFun."""

    uqtestfun_instance, uqtestfun_dict = uqtestfun

    # Assertions
    assert uqtestfun_instance.name == uqtestfun_dict["name"]
    assert uqtestfun_instance.evaluate == uqtestfun_dict["evaluate"]
    assert uqtestfun_instance.spatial_dimension == \
           uqtestfun_dict["input"].spatial_dimension
    assert uqtestfun_instance.parameters == uqtestfun_dict["parameters"]


def test_call_instance(uqtestfun):
    """Test calling an instance of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    xx = np.random.rand(1000, uqtestfun_instance.spatial_dimension)

    # Assertions
    assert_call(uqtestfun_instance, xx)
    assert_call(uqtestfun_instance.evaluate, xx, uqtestfun_instance.parameters)


def test_str(uqtestfun):
    """Test the __str__ method of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    str_ref = f"Name              : {uqtestfun_instance.name}\n" \
              f"Spatial dimension : {uqtestfun_instance.spatial_dimension}\n" \
              f"Evaluate          : {uqtestfun_instance.evaluate.__module__}." \
              f"{uqtestfun_instance.evaluate.__name__}" \
              f"{signature(uqtestfun_instance.evaluate)}"

    assert uqtestfun_instance.__str__() == str_ref


def test_unsupported_fun():
    """Test getting the default arguments of an unsupported test function."""
    with pytest.raises(KeyError):
        get_default_args(create_random_alphanumeric(10))
