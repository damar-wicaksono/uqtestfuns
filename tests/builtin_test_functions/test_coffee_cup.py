"""
Test module for the Coffee Cup model.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from conftest import assert_call
from uqtestfuns.test_functions import CoffeeCup


@pytest.mark.parametrize(
    "solve_ivp_kwargs", [{"method": "RK23"}, {"dense_output": True}]
)
def test_solve_ivp_kwargs(solve_ivp_kwargs):
    """Test passing additional kwargs for solve_ivp."""

    # Create an instance
    fun = CoffeeCup()

    # Add the new parameter
    fun.parameters.add("solve_ivp", solve_ivp_kwargs)

    # Generate test points
    xx = fun.prob_input.get_sample(10)

    # Assertion
    assert_call(fun, xx)


@pytest.mark.parametrize("n_ts", [10, 20, 50])
def test_parameter_nts(n_ts):
    # Create an instance
    fun = CoffeeCup()

    # Modify the parameters
    fun.parameters["n_ts"] = n_ts

    # Generate test points
    xx = fun.prob_input.get_sample(10)

    # Evaluate the function
    yy = fun(xx)

    # Assertions
    assert yy.shape[1] == n_ts
    assert fun.output_dimension == n_ts


@pytest.mark.parametrize("temp_0", [50.0, 60.0, 70.0])
def test_parameter_temp0(temp_0):
    # Create an instance
    fun = CoffeeCup()

    # Modify the parameter
    fun.parameters["temp_0"] = temp_0

    # Generate test points
    xx = fun.prob_input.get_sample(10)

    # Evaluate the function
    yy = fun(xx)

    # Assertions
    assert np.all(yy[:, 0] == temp_0)
