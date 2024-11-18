"""
Test module for instances of the available UQ test functions.

Notes
-----
- All UQ test functions are derived from UQTestFunABC abstract base class.
- The tests in this module only deal with the general behaviors of the concrete
  implementations not about the correctness of computation of a particular
  implementation.
"""

import numpy as np
import pytest
import copy

from typing import Type

from conftest import assert_call

from uqtestfuns.utils import get_available_classes
from uqtestfuns import test_functions, UQTestFunABC

AVAILABLE_FUNCTION_CLASSES = get_available_classes(test_functions)


@pytest.fixture(params=AVAILABLE_FUNCTION_CLASSES)
def builtin_testfun(request) -> Type[UQTestFunABC]:
    _, testfun = request.param

    return testfun


def test_create_instance(builtin_testfun):
    """Test the creation of the default instance of avail. test functions."""
    testfun = builtin_testfun

    # Assertion
    assert_call(testfun)


def test_create_instance_with_custom_name(builtin_testfun):
    """Test the creation of an instance and passing the name argument."""
    testfun_class = builtin_testfun

    # Get the default name of the test function
    function_id = testfun_class.__name__

    # Create a default instance
    my_fun = testfun_class()

    # Assertion
    assert my_fun.function_id == function_id

    # Use custom name to create a test function
    my_fun = testfun_class(function_id=function_id)
    assert my_fun.function_id == function_id


def test_create_instance_with_prob_input(builtin_testfun):
    """Test the creation of a default instance and passing prob. input.

    Notes
    -----
    - If non-default probabilistic input is to be specified, first create
      an instance without probabilistic input then assign the input after
      construction.
    """
    testfun_class = builtin_testfun

    # Create an instance
    my_fun = testfun_class()

    # Copy the underlying probabilistic input
    my_prob_input = copy.copy(my_fun.prob_input)

    # Create an instance without probabilistic input
    if testfun_class.available_inputs is not None:
        my_fun_2 = testfun_class()

        # Assign the probabilistic input
        my_fun_2.prob_input = my_prob_input
        assert my_fun_2.prob_input is my_prob_input

        # Nonsensical probabilistic input model
        with pytest.raises(TypeError):
            my_fun_2.prob_input = 10


def test_create_instance_with_parameters(builtin_testfun):
    """Test the creation of the default instance and passing parameters.

    Notes
    -----
    - If non-default parameters are to be specified, first create
      an instance without parameters then assign the parameters after
      construction.
    """

    testfun_class = builtin_testfun

    my_fun = testfun_class()
    parameters = my_fun.parameters

    if testfun_class.available_parameters is not None:
        my_fun_2 = testfun_class()
        my_fun_2.parameters = parameters
        assert my_fun_2.parameters is parameters
    else:
        assert len(my_fun.parameters) == 0


def test_available_inputs(builtin_testfun):
    """Test creating test functions with different built-in input specs."""

    testfun_class = builtin_testfun

    available_inputs = testfun_class.available_inputs

    for available_input in available_inputs:
        assert_call(testfun_class, input_id=available_input)


def test_available_parameters(builtin_testfun):
    """Test creating test functions with different built-in parameters."""

    testfun_class = builtin_testfun

    available_parameters = testfun_class.available_parameters

    if available_parameters is not None:
        for available_parameter in available_parameters:
            assert_call(testfun_class, parameters_id=available_parameter)


def test_call_instance(builtin_testfun):
    """Test calling an instance of the test function on input values."""

    testfun = builtin_testfun

    # Create an instance
    my_fun = testfun()

    xx = my_fun.prob_input.get_sample(10)

    # Assertions
    assert_call(my_fun, xx)


def test_str(builtin_testfun):
    """Test the __str__() method of a test function instance."""

    # Create an instance
    my_fun = builtin_testfun()

    if my_fun.variable_dimension:
        input_dim = f"{my_fun.input_dimension} (variable)"
    else:
        input_dim = f"{my_fun.input_dimension} (fixed)"
    tags = ", ".join(my_fun.tags)
    str_ref = (
        f"Function ID      : {my_fun.function_id}\n"
        f"Input Dimension  : {input_dim}\n"
        f"Output Dimension : {my_fun.output_dimension}\n"
        f"Parameterized    : {bool(my_fun.parameters)}\n"
        f"Description      : {my_fun.description}\n"
        f"Applications     : {tags}"
    )

    assert my_fun.__str__() == str_ref


def test_str_prob_input(builtin_testfun):
    """Test the __str__() method of the input attached to a test function."""
    # Create an instance
    my_fun = builtin_testfun()

    # str of the ProbInput
    my_prob_input_str = my_fun.prob_input.__str__()

    # Assertion
    assert isinstance(my_prob_input_str, str)


def test_transform_input(builtin_testfun):
    """Test transforming a set of input values in the default unif. domain."""

    testfun = builtin_testfun
    rng_seed = 32

    # Create an instance
    my_fun = testfun()
    my_fun.prob_input.reset_rng(rng_seed)

    sample_size = 100

    # Transformation from the default uniform domain to the input domain
    rng = np.random.default_rng(rng_seed)
    xx_1 = -1 + 2 * rng.random((sample_size, my_fun.input_dimension))
    xx_1 = my_fun.transform_sample(xx_1)

    # Directly sample from the input property
    xx_2 = my_fun.prob_input.get_sample(sample_size)

    # Assertion: Both samples are equal because the seed is identical
    assert np.allclose(xx_1, xx_2)


def test_transform_input_non_default(builtin_testfun):
    """Test transforming an input from non-default domain."""

    testfun = builtin_testfun
    rng_seed = 1232

    # Create an instance
    my_fun = testfun()
    my_fun.prob_input.reset_rng(rng_seed)

    sample_size = 100

    # Transformation from non-default uniform domain to the input domain
    rng = np.random.default_rng(rng_seed)
    xx_1 = rng.random((sample_size, my_fun.input_dimension))
    xx_1 = my_fun.transform_sample(xx_1, min_value=0.0, max_value=1.0)

    # Directly sample from the input property
    xx_2 = my_fun.prob_input.get_sample(sample_size)

    # Assertion: Both samples are equal because the seed is identical
    assert np.allclose(xx_1, xx_2)


def test_evaluate_wrong_input_dim(builtin_testfun):
    """Test if an exception is raised when input is of wrong dimension."""

    testfun = builtin_testfun()

    xx = np.random.rand(10, testfun.input_dimension * 2)

    with pytest.raises(ValueError):
        testfun(xx)


def test_evaluate_wrong_input_domain(builtin_testfun):
    """Test if an exception is raised when sampled input is in wrong domain."""

    testfun = builtin_testfun()

    # Create a sample in [-2, 2]
    xx = -2 + 4 * np.random.rand(1000, testfun.input_dimension)

    with pytest.raises(ValueError):
        # By default, the transformation domain is from [-1, 1]
        testfun.transform_sample(xx)

    # Create sampled input values from the default and perturb them
    xx = np.empty((100, testfun.input_dimension))
    for i, marginal in enumerate(testfun.prob_input.marginals):
        lb = marginal.lower + 1000
        ub = marginal.upper - 1000
        xx[:, i] = lb + (ub - lb) * np.random.rand(100)

    with pytest.raises(ValueError):
        # Evaluation will check if the sampled input are within the domain
        testfun(xx)


def test_evaluate_invalid_input_dim(builtin_testfun):
    """Test if an exception is raised if invalid input dimension is given."""

    if hasattr(builtin_testfun, "default_input_dimension"):
        with pytest.raises(TypeError):
            builtin_testfun(input_dimension="10")


def test_evaluate_invalid_input_selection(builtin_testfun):
    """Test if an exception is raised if invalid input selection is given."""
    with pytest.raises(KeyError):
        builtin_testfun(input_id=100)
