"""
Test module for UQTestFun class, a generic class for generic UQ test function.
"""

import numpy as np
import pytest

from typing import Callable, Optional
from typing_extensions import TypedDict

from uqtestfuns.core.uqtestfun import UQTestFun
from uqtestfuns.core.prob_input.probabilistic_input_new import ProbInput
from uqtestfuns.core.prob_input.marginal import Marginal
from uqtestfuns.core.parameters import Parameters
from conftest import assert_call, create_random_marginals


class UQTestFunArgs(TypedDict):
    evaluate: Callable
    prob_input: ProbInput
    parameters: Optional[Parameters]
    name: str


@pytest.fixture(params=[True, False], ids=["w/_parameters", "w/o_parameters"])
def uqtestfun(request):
    """Create an instance of UQTestFun with or without parameters."""
    input_marginals = create_random_marginals(1)

    def evaluate(x, **kwargs):
        p = kwargs.get("p", 1.0)
        return p * (np.sum(x, axis=1) + 1)

    if request.param:
        parameters = Parameters({"p": 10.0})
    else:
        parameters = None

    my_args: UQTestFunArgs = {
        "evaluate": evaluate,
        "prob_input": ProbInput(input_marginals),
        "parameters": parameters,
        "name": "TestFunction",
    }

    uqtestfun_instance = UQTestFun(**my_args)

    return uqtestfun_instance, my_args


def test_create_instance(uqtestfun):
    """Test the creation of an instance of UQTestFun."""

    uqtestfun_instance, uqtestfun_dict = uqtestfun

    # Assertions
    assert uqtestfun_instance.name == uqtestfun_dict["name"]
    # The original evaluate function is stored in a hidden attribute
    assert uqtestfun_instance._evaluate == uqtestfun_dict["evaluate"]
    assert (
        uqtestfun_instance.input_dimension
        == uqtestfun_dict["prob_input"].dimension
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

    s = str(uqtestfun_instance)

    name = uqtestfun_instance.name
    if name is None:
        name = "N/A"
    description = uqtestfun_instance.description
    if description is None:
        description = "N/A"

    # Assertions
    assert name in s
    assert description in s
    assert str(uqtestfun_instance.input_dimension) in s
    assert str(uqtestfun_instance.output_dimension) in s
    assert str(uqtestfun_instance.parameters is not None) in s


def test_repr(uqtestfun):
    """Test the __repr__ method of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    parameters_id = (
        uqtestfun_instance._parameters.name
        if uqtestfun_instance._parameters is not None
        else None
    )

    repr_ref = (
        f"<UQTestFun "
        f"name={uqtestfun_instance.name!r}, "
        f"input_dimension={uqtestfun_instance.input_dimension}, "
        f"input_id={uqtestfun_instance.prob_input.name!r}, "
        f"parameters_id={parameters_id!r}"
        f">"
    )

    assert uqtestfun_instance.__repr__() == repr_ref


def test_get_sample(uqtestfun):
    """Test the get_sample method of UQTestFun."""
    uqtestfun_instance, _ = uqtestfun

    sample_size = 10
    yy = uqtestfun_instance.get_sample(sample_size)

    if uqtestfun_instance.output_dimension == 1:
        assert yy.shape == (sample_size,)
    else:
        assert yy.shape == (sample_size, uqtestfun_instance.output_dimension)


def test_invalid_input(uqtestfun):
    """Test using an invalid input to construct a UQTestFun instance."""
    _, uqtestfun_dict = uqtestfun

    # Using an invalid type of input for the test function
    uqtestfun_dict["prob_input"] = "Test"

    with pytest.raises(TypeError):
        UQTestFun(**uqtestfun_dict)


def test_invalid_evaluate(uqtestfun):
    """Test using an invalid evaluate function to construct an instance."""
    _, uqtestfun_args = uqtestfun

    # Create an instance
    with pytest.raises(TypeError):
        _ = UQTestFun(
            evaluate=5,  # type: ignore
            prob_input=uqtestfun_args["prob_input"],
            parameters=uqtestfun_args["parameters"],
            name=uqtestfun_args["name"],
        )


def test_invalid_parameters(uqtestfun):
    """Test using invalid parameters to construct a UQTestFun instance."""
    _, uqtestfun_args = uqtestfun

    # Create an instance
    with pytest.raises(TypeError):
        _ = UQTestFun(
            evaluate=uqtestfun_args["evaluate"],
            prob_input=uqtestfun_args["prob_input"],
            parameters=5,  # type: ignore
            name=uqtestfun_args["name"],
        )


def test_invalid_output_shape():
    """Test using an invalid output shape from evaluate function."""

    def evaluate(xx):
        return np.sum(xx, axis=1)

    prob_input = ProbInput([Marginal("uniform", [0, 1])])

    uqtestfun_ = UQTestFun(
        evaluate=evaluate,
        prob_input=prob_input,
        parameters=None,
        output_dimension=2,
    )

    with pytest.raises(ValueError):
        _ = uqtestfun_.get_sample(10)


def test_invalid_input_shape(uqtestfun):
    """Test using an invalid input shape from evaluate function."""
    uqtestfun_instance, _ = uqtestfun

    # Generate input of higher dimension
    rng = np.random.default_rng()
    xx = rng.random((10, uqtestfun_instance.input_dimension + 1))

    with pytest.raises(ValueError):
        _ = uqtestfun_instance(xx)


def test_invalid_input_domain(uqtestfun):
    """Test using an invalid input domain from evaluate function."""
    uqtestfun_instance, _ = uqtestfun

    # Array of an invalid domain
    sample_size = 100
    xx = np.full((sample_size, uqtestfun_instance.input_dimension), np.inf)

    with pytest.raises(ValueError):
        _ = uqtestfun_instance(xx)
