"""
Test module for the Sobol'-Levitan test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns.test_functions import SobolLevitan

available_parameters = list(SobolLevitan.available_parameters.keys())


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(KeyError):
        SobolLevitan(parameters_id="marelli1")


@pytest.mark.parametrize("input_dimension", [1, 2, 3, 10, 21])
@pytest.mark.parametrize("parameters_id", available_parameters)
def test_compute_mean(input_dimension, parameters_id):
    """Test the mean computation as the result is analytical."""

    # Create an instance of Sobol'-Levitan test function
    my_fun = SobolLevitan(
        input_dimension=input_dimension,
        parameters_id=parameters_id,
    )

    # Compute mean via Monte Carlo
    xx = my_fun.prob_input.get_sample(1000000)
    yy = my_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = my_fun.parameters["c0"]

    # Compare it relative to the standard deviation
    mean_mc_rel = mean_mc / np.std(yy)

    # Assertion (no need to be very ambitious with the tolerance)
    if mean_ref == 0:
        assert np.abs(mean_mc_rel) < 1e-1
    else:
        assert np.allclose(mean_mc_rel, mean_ref, rtol=1e-1)


@pytest.mark.parametrize("input_dimension", [1, 2, 3, 10, 21])
@pytest.mark.parametrize("parameters_id", available_parameters)
def test_compute_variance(input_dimension, parameters_id):
    """Test the variance computation as the result is analytical."""

    # Create an instance of the Sobol'-Levitan test function
    my_fun = SobolLevitan(
        input_dimension=input_dimension,
        parameters_id=parameters_id,
    )

    # Compute the variance via Monte Carlo
    xx = my_fun.prob_input.get_sample(1000000)
    yy = my_fun(xx)

    var_mc = np.var(yy)

    # Analytical variance
    bb = my_fun.parameters["bb"]

    def _h_m(bb):
        out = 1.0
        for b in bb:
            if b == 0:
                out *= 1.0
            else:
                out *= (np.exp(2 * b) - 1) / 2 / b
        return out

    def _i_m(bb):
        out = 1.0
        for b in bb:
            if b == 0:
                out *= 1.0
            else:
                out *= (np.exp(b) - 1) / b
        return out

    var_ref = _h_m(bb) - _i_m(bb) ** 2

    # Assertion (no need to be very ambitious with the tolerance)
    assert np.allclose(var_mc, var_ref, rtol=1e-1)
