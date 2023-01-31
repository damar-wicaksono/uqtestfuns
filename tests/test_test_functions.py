"""
Test module for instances of the available UQ test functions.

Notes
-----
- All UQ test functions are instantiated as UQTestFun.
- The tests in this module only deal with the behavior of the UQTestFun
  instances associated with the UQ test functions not about the correctness
  of the computation results.
"""
import numpy as np
import pytest

from typing import Callable

from uqtestfuns import create_from_default
from conftest import assert_call

from uqtestfuns.test_functions.default import AVAILABLE_FUNCTIONS

AVAILABLE_FUNCTION_KEYS = list(AVAILABLE_FUNCTIONS.keys())


@pytest.fixture(params=AVAILABLE_FUNCTION_KEYS)
def default_testfun(request):
    """Fixture for the tests, an instance from the avail. test functions."""
    testfun = create_from_default(request.param)
    testfun_mod = AVAILABLE_FUNCTIONS[request.param]

    return testfun, testfun_mod


def test_create_instance(default_testfun):
    """Test the creation of the default instance of avail. test functions."""

    testfun, testfun_mod = default_testfun

    default_input = testfun_mod.DEFAULT_INPUTS[
        testfun_mod.DEFAULT_INPUT_SELECTION
    ]

    if isinstance(default_input, Callable):  # type: ignore
        default_input = default_input(testfun_mod.DEFAULT_DIMENSION)
    else:
        default_input = default_input

    # Assertions
    assert testfun.spatial_dimension == default_input.spatial_dimension

    # TODO: Implement a better equality for the input dataclass
    # assert testfun.input == testfun_mod.DEFAULT_INPUT


def test_call_instance(default_testfun):
    """Test calling an instance of the test function."""

    testfun, _ = default_testfun

    xx = testfun.prob_input.get_sample(10)

    # Assertions
    assert_call(testfun, xx)


def test_transform_input(default_testfun):
    """Test transforming a set of input values in the default unif. domain."""

    testfun, _ = default_testfun

    sample_size = 100

    # Transformation from the default uniform domain to the input domain
    np.random.seed(315)
    # NOTE: Direct sample from the input property is done by column to column,
    # for reproducibility using the same RNG seed the reference input must be
    # filled in column by column as well with the. The call to NumPy random
    # number generators below yields the same effect.
    xx_1 = -1 + 2 * np.random.rand(testfun.spatial_dimension, sample_size).T
    xx_1 = testfun.transform_sample(xx_1)

    # Directly sample from the input property
    np.random.seed(315)
    xx_2 = testfun.prob_input.get_sample(sample_size)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_transform_input_non_default(default_testfun):
    """Test transforming an input from non-default domain."""

    testfun, _ = default_testfun

    sample_size = 100

    # Transformation from non-default uniform domain to the input domain
    np.random.seed(315)
    # NOTE: Direct sample from the input property is done by column to column,
    # for reproducibility using the same RNG seed the reference input must be
    # filled in column by column as well with the. The call to NumPy random
    # number generators below yields the same effect.
    xx_1 = np.random.rand(testfun.spatial_dimension, sample_size).T
    xx_1 = testfun.transform_sample(xx_1, min_value=0.0, max_value=1.0)

    # Directly sample from the input property
    np.random.seed(315)
    xx_2 = testfun.prob_input.get_sample(sample_size)

    # Assertion: two sampled values are equal
    assert np.allclose(xx_1, xx_2)


def test_wrong_input_dim(default_testfun):
    """Test if an exception is raised when input is of wrong dimension."""

    testfun, _ = default_testfun

    xx = np.random.rand(10, testfun.spatial_dimension * 2)

    with pytest.raises(ValueError):
        testfun(xx)


def test_wrong_input_domain(default_testfun):
    """Test if an exception is raised when sampled input is of wrong domain."""

    testfun, _ = default_testfun

    # Create a sample in [-2, 2]
    xx = -2 + 4 * np.random.rand(1000, testfun.spatial_dimension)

    with pytest.raises(ValueError):
        # By default, the transformation domain is from [-1, 1]
        testfun.transform_sample(xx)

    # Create sampled input values from the default and perturb them
    xx = np.empty((100, testfun.spatial_dimension))
    for i, marginal in enumerate(testfun.prob_input.marginals):
        lb = marginal.lower + 1000
        ub = marginal.upper - 1000
        xx[:, i] = lb + (ub - lb) * np.random.rand(100)

    with pytest.raises(ValueError):
        # Evaluation will check if the sampled input are within the domain
        testfun(xx)


@pytest.mark.parametrize("test_function", AVAILABLE_FUNCTION_KEYS)
def test_invalid_input_params_selection(test_function):
    """"""
    with pytest.raises(ValueError):
        create_from_default(test_function, input_selection="qlej2")
