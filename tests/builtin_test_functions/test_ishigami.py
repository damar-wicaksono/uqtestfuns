"""
Test module for the Ishigami test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns import Ishigami

# Test for different parameters to the Ishigami function
available_parameters = list(Ishigami.available_parameters.keys())


@pytest.fixture(params=available_parameters)
def ishigami_fun(request):
    ishigami = Ishigami(parameters_selection=request.param)

    return ishigami


def test_compute_mean(ishigami_fun):
    """Test the mean computation as the result is analytical."""

    # Compute mean via Monte Carlo
    xx = ishigami_fun.prob_input.get_sample(1000000)
    yy = ishigami_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = ishigami_fun.parameters["a"] / 2

    # Assertion
    assert np.allclose(mean_mc, mean_ref, rtol=1e-2)


def test_compute_variance(ishigami_fun):
    """Test the variance computation as the result is analytical."""

    # Compute variance via Monte Carlo
    xx = ishigami_fun.prob_input.get_sample(1000000)
    yy = ishigami_fun(xx)

    var_mc = np.var(yy)

    # Analytical mean
    a, b = ishigami_fun.parameters["a"], ishigami_fun.parameters["b"]
    var_ref = a**2 / 8 + b * np.pi**4 / 5 + b**2 * np.pi**8 / 18 + 0.5

    # Assertion
    assert np.allclose(var_mc, var_ref, rtol=1e-2)


@pytest.mark.parametrize("param_selection", available_parameters)
def test_different_parameters(param_selection):
    """Test selecting different built-in parameters."""

    # Create an instance of Ishigami function with a specified param. selection
    my_testfun_1 = Ishigami(parameters_selection=param_selection)
    my_testfun_2 = Ishigami(parameters_selection=param_selection)

    # Assertion
    assert my_testfun_1.parameters == my_testfun_2.parameters


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(KeyError):
        Ishigami(parameters_selection="marelli1")
