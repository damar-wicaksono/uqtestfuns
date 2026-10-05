"""
Test module for the Coffee Cup model.

Notes
-----
- The tests defined in this module deal with the correctness of the evaluation.
"""

import numpy as np
import pytest

from conftest import assert_call
from uqtestfuns import CoffeeCup


@pytest.mark.parametrize(
    "solve_ivp_kwargs", [{"method": "RK23"}, {"dense_output": True}]
)
def test_solve_ivp_kwargs(solve_ivp_kwargs):
    """Test passing additional kwargs for solve_ivp."""

    # Create an instance
    fun = CoffeeCup(parameters=CoffeeCup().parameters.copy())

    # Create the new parameter
    fun.parameters["solve_ivp_kwargs"] = solve_ivp_kwargs

    # Generate test points
    xx = fun.prob_input.get_sample(10)

    # Assertion
    assert_call(fun, xx)


@pytest.mark.parametrize("temp_0", [50.0, 60.0, 70.0])
def test_parameter_temp0(temp_0):
    # Create an instance
    fun = CoffeeCup(parameters=CoffeeCup().parameters.copy())

    # Add the new parameter
    fun.parameters["temp_0"] = temp_0

    # Generate test points
    xx = fun.prob_input.get_sample(10)

    # Evaluate the function
    yy = fun(xx)

    # Assertions
    assert np.all(yy[:, 0] == temp_0)
