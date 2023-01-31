"""
Test module for the Sobol-G test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import numpy as np
import pytest

import uqtestfuns
from uqtestfuns.test_functions import sobol_g as sobol_g_mod


@pytest.mark.parametrize(
    "parameter", [None] + list(sobol_g_mod.AVAILABLE_PARAMETERS.keys())
)
def test_different_parameters(parameter):
    """Test selecting different built-in parameters."""

    # Create an instance of a test function with a specified param. selection
    my_fun = uqtestfuns.create_from_default("sobol-g", parameters=parameter)

    # Assertion
    if parameter:
        stored_parameters = sobol_g_mod.AVAILABLE_PARAMETERS[parameter](
            my_fun.spatial_dimension
        )
        assert np.allclose(my_fun.parameters, stored_parameters)
    else:
        default_selection = sobol_g_mod.DEFAULT_PARAMETERS_SELECTION
        stored_parameters = sobol_g_mod.AVAILABLE_PARAMETERS[
            default_selection
        ](sobol_g_mod.DEFAULT_DIMENSION)
        assert np.allclose(my_fun.parameters, stored_parameters)


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(ValueError):
        uqtestfuns.create_from_default("sobol-g", parameters="marelli1")


# ATTENTION: some parameters choice (e.g., "sobol-1")
# can't be estimated properly with low N at high dimension
@pytest.mark.parametrize("spatial_dimension", [None, 1, 2, 10])
@pytest.mark.parametrize(
    "parameter", [None] + list(sobol_g_mod.AVAILABLE_PARAMETERS.keys())
)
def test_compute_mean(spatial_dimension, parameter):
    """Test the mean computation as the result is analytical."""

    # Create an instance of Sobol-G test function
    my_fun = uqtestfuns.create_from_default(
        "sobol-g",
        spatial_dimension=spatial_dimension,
        parameters=parameter,
    )

    # Compute mean via Monte Carlo
    xx = my_fun.prob_input.get_sample(500000)
    yy = my_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = 1.0

    # Assertion (no need to be very ambitious with the tolerance)
    assert np.allclose(mean_mc, mean_ref, rtol=1e-1)


# ATTENTION: parameters with "Sobol-1" is unstable at large dimension >= 15
@pytest.mark.parametrize("spatial_dimension", [None, 1, 2, 10])
@pytest.mark.parametrize(
    "parameter", [None] + list(sobol_g_mod.AVAILABLE_PARAMETERS.keys())
)
def test_compute_variance(spatial_dimension, parameter):
    """Test the variance computation as the result is analytical."""

    # Create an instance of the Sobol-G test function
    my_fun = uqtestfuns.create_from_default(
        "sobol-g",
        spatial_dimension=spatial_dimension,
        parameters=parameter,
    )

    # Compute the variance via Monte Carlo
    xx = my_fun.prob_input.get_sample(500000)
    yy = my_fun(xx)

    var_mc = np.var(yy)

    # Analytical variance
    params = my_fun.parameters
    var_ref = (
        np.prod((4 / 3 + 2 * params + params**2) / (1 + params) ** 2) - 1
    )

    # Assertion (no need to be very ambitious with the tolerance)
    assert np.allclose(var_mc, var_ref, rtol=1e-1)
