"""
Test module for the Ackley test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns import Rosenbrock


def test_one_dimensional():
    """Test evaluating the one-dimensional Rosenbrock function."""
    my_fun = Rosenbrock(input_dimension=1)

    xx = my_fun.prob_input.get_sample(100)
    yy = my_fun(xx)

    # One-dimensional Rosenbrock always returns zero
    assert np.allclose(yy, 0.0)


@pytest.mark.parametrize("input_dimension", [2, 3, 10])
def test_optimum_value_a_eq_1(input_dimension):
    """Test the optimum value, regardless of the dimension, when a == 1."""
    my_fun = Rosenbrock(input_dimension=input_dimension)

    xx = np.ones((1, my_fun.input_dimension))
    yy = my_fun(xx)

    # For a == 0, The optima of the Ackley function is at 1.0s
    assert np.allclose(yy, 0.0)


@pytest.mark.parametrize("input_dimension", [2, 3, 10])
def test_optimum_value_a_eq_0(input_dimension):
    """Test the optimum value, regardless of the dimension, when a == 0"""
    my_fun = Rosenbrock(input_dimension=input_dimension)
    my_fun.parameters["a"] = 0.0

    # The optima of the function when a = 0 is not at 1.0's
    xx = np.ones((1, my_fun.input_dimension))
    yy = my_fun(xx)

    assert not np.allclose(yy, 0.0)

    # but at 0.0's
    xx = np.zeros((1, my_fun.input_dimension))
    yy = my_fun(xx)

    assert np.allclose(yy, 0.0)
