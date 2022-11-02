"""
Test module for the Ishigami test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import numpy as np
import pytest

from uqtestfuns import UQTestFun, get_default_args
from uqtestfuns.test_functions import ishigami as ishigami_mod


# Test for different parameters to the Ishigami function
parameters = [ishigami_mod.DEFAULT_PARAMETERS, (7.0, 0.05)]


@pytest.fixture(params=parameters)
def ishigami_fun(request):
    default_args = get_default_args("ishigami")
    ishigami = UQTestFun(
        name=default_args["name"],
        evaluate=default_args["evaluate"],
        input=default_args["input"],
        parameters=request.param,
    )

    return ishigami


def test_compute_mean(ishigami_fun):
    """Test the mean computation as the result is analytical."""

    # Compute mean via Monte Carlo
    xx = ishigami_fun.input.get_sample(1000000)
    yy = ishigami_fun(xx)

    mean_mc = np.mean(yy)

    # Analytical mean
    mean_ref = ishigami_fun.parameters[0] / 2

    # Assertion
    assert np.allclose(mean_mc, mean_ref, rtol=1e-2)


def test_compute_variance(ishigami_fun):
    """Test the variance computation as the result is analytical."""

    # Compute variance via Monte Carlo
    xx = ishigami_fun.input.get_sample(1000000)
    yy = ishigami_fun(xx)

    var_mc = np.var(yy)

    # Analytical mean
    a, b = ishigami_fun.parameters
    var_ref = a**2 / 8 + b * np.pi**4 / 5 + b**2 * np.pi**8 / 18 + 0.5

    # Assertion
    assert np.allclose(var_mc, var_ref, rtol=1e-2)
