import numpy as np
import pytest

from uqtestfuns import UQTestFun, get_default_args
from uqtestfuns.test_functions import ishigami as ishigami_mod
from conftest import assert_call


# Test for different parameters to the Ishigami function
parameters = [ishigami_mod.DEFAULT_PARAMETERS, (7.0, 0.05)]


@pytest.fixture(params=parameters)
def ishigami_fun(request):
    default_args = get_default_args("ishigami")
    ishigami = UQTestFun(
        name=default_args["name"],
        evaluate=default_args["evaluate"],
        input=default_args["input"],
        parameters=request.param
    )

    return ishigami


def test_create_instance(ishigami_fun):
    """Test the creation of the default instance of the Ishigami function."""

    # Assertions
    assert ishigami_fun.spatial_dimension == \
           ishigami_mod.DEFAULT_INPUT.spatial_dimension
    assert ishigami_fun.input == ishigami_mod.DEFAULT_INPUT


def test_call_instance(ishigami_fun):
    """Test calling an instance of the test function."""

    xx = np.random.rand(10, ishigami_fun.spatial_dimension)

    # Assertions
    assert_call(ishigami_fun, xx)
    assert_call(ishigami_fun.evaluate, xx)
    assert_call(ishigami_fun.evaluate, xx, ishigami_mod.DEFAULT_PARAMETERS)


def test_transform_input(ishigami_fun):
    """Test transforming an input."""

    # Transformation from the default uniform domain to the input domain.
    np.random.seed(315)
    xx_1 = -1 + 2 * np.random.rand(100, ishigami_fun.spatial_dimension)
    xx_1 = ishigami_fun.transform_inputs(xx_1)

    # Directly sample from the input property.
    np.random.seed(315)
    xx_2 = ishigami_fun.input.get_sample(100)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_transform_input_non_default(ishigami_fun):
    """Test transforming an input from non-default domain."""

    # Transformation from non-default uniform domain to the input domain.
    np.random.seed(315)
    xx_1 = np.random.rand(100, ishigami_fun.spatial_dimension)
    xx_1 = ishigami_fun.transform_inputs(xx_1, min_value=0.0, max_value=1.0)

    # Directly sample from the input property.
    np.random.seed(315)
    xx_2 = ishigami_fun.input.get_sample(100)

    # Assertion: two sampled values are equal.
    assert np.allclose(xx_1, xx_2)


def test_wrong_input_dim(ishigami_fun):
    """Test if an exception is raised when input is of wrong dimension."""

    # Compute variance via Monte Carlo
    xx = np.random.rand(10, ishigami_fun.spatial_dimension*2)

    with pytest.raises(ValueError):
        ishigami_fun(xx)


def test_compute_mean(ishigami_fun):
    """Test the mean computation as the result is analytical."""

    # Compute mean via Monte Carlo
    xx = ishigami_fun.input.get_sample(1000000)
    yy = ishigami_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = ishigami_fun.parameters[0] / 2

    # Assertion
    assert np.allclose(mean_mc, mean_ref, rtol=1e-3)


def test_compute_variance(ishigami_fun):
    """Test the variance computation as the result is analytical."""

    # Compute variance via Monte Carlo
    xx = ishigami_fun.input.get_sample(1000000)
    yy = ishigami_fun(xx)

    var_mc = np.var(yy)

    # Analytical mean
    a, b = ishigami_fun.parameters
    var_ref = a**2 / 8 + b * np.pi**4/5 + b**2 * np.pi**8/18 + 0.5

    # Assertion
    assert np.allclose(var_mc, var_ref, rtol=1e-3)
