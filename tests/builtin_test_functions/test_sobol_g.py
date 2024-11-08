"""
Test module for the Sobol-G test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns.test_functions import SobolG

available_parameters = list(SobolG.available_parameters.keys())


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(KeyError):
        SobolG(parameters_id="marelli1")


# ATTENTION: some parameters choice (e.g., "sobol-1")
# can't be estimated properly with low N at high dimension
@pytest.mark.parametrize("input_dimension", [1, 2, 3, 10])
@pytest.mark.parametrize("params_selection", available_parameters)
def test_compute_mean(input_dimension, params_selection):
    """Test the mean computation as the result is analytical."""

    # Create an instance of Sobol-G test function
    my_fun = SobolG(
        input_dimension=input_dimension,
        parameters_id=params_selection,
    )

    # Assert that ProbInput is correctly attached
    assert my_fun.prob_input is not None

    # Compute mean via Monte Carlo
    xx = my_fun.prob_input.get_sample(1000000)
    yy = my_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = 1.0

    # Assertion (no need to be very ambitious with the tolerance)
    assert np.allclose(mean_mc, mean_ref, rtol=1e-1)


# ATTENTION: parameters with "Sobol-1" is unstable at large dimension >= 15
@pytest.mark.parametrize("input_dimension", [1, 2, 3, 10])
@pytest.mark.parametrize("params_selection", available_parameters)
def test_compute_variance(input_dimension, params_selection):
    """Test the variance computation as the result is analytical."""

    # Create an instance of the Sobol-G test function
    my_fun = SobolG(
        input_dimension=input_dimension,
        parameters_id=params_selection,
    )

    # Assert that ProbInput is correctly attached
    assert my_fun.prob_input is not None

    # Compute the variance via Monte Carlo
    xx = my_fun.prob_input.get_sample(500000)
    yy = my_fun(xx)

    var_mc = np.var(yy)

    # Analytical variance
    params = my_fun.parameters["aa"]
    var_ref = np.prod((4 / 3 + 2 * params + params**2) / (1 + params) ** 2) - 1

    # Assertion (no need to be very ambitious with the tolerance)
    assert np.allclose(var_mc, var_ref, rtol=1e-1)
