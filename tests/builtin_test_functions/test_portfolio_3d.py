"""
Test module for the simple portfolio model.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns import Portfolio3D

# Test for different sets of parameters of the simple portfolio model
available_parameters = list(Portfolio3D.available_parameters.keys())


@pytest.fixture(params=available_parameters)
def portfolio3d_fun(request):
    portfolio3d = Portfolio3D(parameters_selection=request.param)

    return portfolio3d


def test_compute_mean(portfolio3d_fun):
    """Test the analytical mean."""

    # Analytical mean
    mean_inputs = np.array(
        [x.parameters[0] for x in portfolio3d_fun.prob_input.marginals]
    )
    parameters = np.array(
        [
            portfolio3d_fun.parameters["cs"],
            portfolio3d_fun.parameters["ct"],
            portfolio3d_fun.parameters["cj"],
        ]
    )
    mean_ref = mean_inputs @ parameters

    # Assertion
    assert np.allclose(mean_ref, 0)


def test_compute_variance(portfolio3d_fun):
    """Test the analytical variance."""

    # Compute variance via Monte Carlo
    xx = portfolio3d_fun.prob_input.get_sample(10000000)
    yy = portfolio3d_fun(xx)

    var_mc = np.var(yy)

    # Analytical variance
    std_inputs = np.array(
        [x.parameters[1] for x in portfolio3d_fun.prob_input.marginals]
    )
    parameters = np.array(
        [
            portfolio3d_fun.parameters["cs"],
            portfolio3d_fun.parameters["ct"],
            portfolio3d_fun.parameters["cj"],
        ]
    )
    var_ref = parameters**2 @ std_inputs**2

    # Assertion
    assert np.allclose(var_mc, var_ref, rtol=1e-1)


@pytest.mark.parametrize("param_selection", available_parameters)
def test_different_parameters(param_selection):
    """Test selecting different built-in parameters."""

    # Create an instance of Ishigami function with a specified param. selection
    my_testfun_1 = Portfolio3D(parameters_selection=param_selection)
    my_testfun_2 = Portfolio3D(parameters_selection=param_selection)

    # Assertion: The parameter sets are identical
    assert my_testfun_1.parameters == my_testfun_2.parameters


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(KeyError):
        Portfolio3D(parameters_selection="marelli1")
