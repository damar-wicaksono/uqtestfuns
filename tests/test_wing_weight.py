import numpy as np
import pytest

from uqtestfuns import UQTestFun, get_default_args
from uqtestfuns.test_functions import wing_weight as wing_weight_mod
from conftest import assert_call


@pytest.fixture
def wing_weight_fun():
    default_args = get_default_args("wing weight")
    wing_weight = UQTestFun(**default_args)

    return wing_weight


def test_create_instance(wing_weight_fun):
    """Test the creation of the default instance of the Wing Weight function."""

    # Assertions
    assert wing_weight_fun.spatial_dimension == \
           wing_weight_mod.DEFAULT_INPUT.spatial_dimension
    assert wing_weight_fun.input == wing_weight_mod.DEFAULT_INPUT


def test_call_instance(wing_weight_fun):
    """Test calling an instance of the test function."""

    xx = np.random.rand(10, wing_weight_fun.spatial_dimension)

    # Assertions
    assert_call(wing_weight_fun, xx)
    assert_call(wing_weight_fun.evaluate, xx)


def test_transform_input(wing_weight_fun):
    """Test transforming an input."""

    # Transformation from the default uniform domain to the input domain
    np.random.seed(315)
    xx_1 = -1 + 2 * np.random.rand(100, wing_weight_fun.spatial_dimension)
    xx_1 = wing_weight_fun.transform_inputs(xx_1)

    # Directly sample from the input property
    np.random.seed(315)
    xx_2 = wing_weight_fun.input.get_sample(100)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_transform_input_non_default(wing_weight_fun):
    """Test transforming an input from non-default domain."""

    # Transformation from non-default uniform domain to the input domain
    np.random.seed(315)
    xx_1 = np.random.rand(100, wing_weight_fun.spatial_dimension)
    xx_1 = wing_weight_fun.transform_inputs(xx_1, min_value=0.0, max_value=1.0)

    # Directly sample from the input property
    np.random.seed(315)
    xx_2 = wing_weight_fun.input.get_sample(100)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_wrong_input_dim(wing_weight_fun):
    """Test if an exception is raised when input is of wrong dimension."""

    # Compute variance via Monte Carlo
    xx = np.random.rand(10, wing_weight_fun.spatial_dimension*2)

    with pytest.raises(ValueError):
        wing_weight_fun(xx)

# TODO: Test the correctness of results