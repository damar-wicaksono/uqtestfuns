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
from uqtestfuns.test_functions import ackley as ackley_mod


# Test for different parameters to the Ackley function
parameters = [ackley_mod.DEFAULT_PARAMETERS, (10., 0.1, 2 * np.pi)]


@pytest.fixture(params=parameters)
def ackley_fun(request):
    default_args = get_default_args("ackley")
    ackley = UQTestFun(
        name=default_args["name"],
        evaluate=default_args["evaluate"],
        input=default_args["input"],
        parameters=request.param,
    )

    return ackley


def test_optimum_value(ackley_fun):
    """Test the optimum value."""

    xx = np.zeros((1, ackley_fun.spatial_dimension))
    yy = ackley_fun(xx)

    assert np.allclose(yy, 0.0)
