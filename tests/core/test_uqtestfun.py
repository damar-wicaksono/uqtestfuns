"""
Test module for UQTestFun class, a generic class for generic UQ test function.
"""

import pytest

from uqtestfuns import UQTestFun, ProbInput, FunParams
from conftest import assert_call, create_random_marginals


@pytest.fixture
def uqtestfun():
    """Create an instance of UQTestFun."""
    input_marginals = create_random_marginals(1)

    def evaluate(x, p):
        return p * (x + 1)

    parameters = FunParams(
        declared_parameters=[{"keyword": "p", "value": 10.0}]
    )

    my_args = {
        "evaluate": evaluate,
        "prob_input": ProbInput(input_marginals),
        "parameters": parameters,
        "function_id": "TestFunction",
    }

    uqtestfun_instance = UQTestFun(
        evaluate=evaluate,
        prob_input=ProbInput(input_marginals),
        parameters=parameters,
        function_id="TestFunction",
    )

    return uqtestfun_instance, my_args


def test_create_instance(uqtestfun):
    """Test the creation of an instance of UQTestFun."""

    uqtestfun_instance, uqtestfun_dict = uqtestfun

    # Assertions
    assert uqtestfun_instance.function_id == uqtestfun_dict["function_id"]
    # The original evaluate function is stored in a hidden attribute
    assert uqtestfun_instance._evaluate == uqtestfun_dict["evaluate"]
    assert (
        uqtestfun_instance.input_dimension
        == uqtestfun_dict["prob_input"].input_dimension
    )
    assert uqtestfun_instance.parameters == uqtestfun_dict["parameters"]


def test_call_instance(uqtestfun):
    """Test calling an instance of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    xx = uqtestfun_instance.prob_input.get_sample(1000)

    # Assertions
    assert_call(uqtestfun_instance, xx)


def test_str(uqtestfun):
    """Test the __str__ method of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    str_ref = (
        f"Function ID      : {uqtestfun_instance.function_id}\n"
        f"Input Dimension  : {uqtestfun_instance.input_dimension}\n"
        f"Output Dimension : {uqtestfun_instance.output_dimension}\n"
        f"Parameterized    : {bool(uqtestfun_instance.parameters)}"
    )

    assert uqtestfun_instance.__str__() == str_ref


def test_invalid_input(uqtestfun):
    """Test using an invalid input to construct a UQTestFun instance."""
    _, uqtestfun_dict = uqtestfun

    # Using an invalid type of input for the test function
    uqtestfun_dict["prob_input"] = "Test"

    with pytest.raises(TypeError):
        UQTestFun(**uqtestfun_dict)
