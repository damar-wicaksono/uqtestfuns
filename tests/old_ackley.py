"""
Test module for the Ackley test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import numpy as np
import pytest

from uqtestfuns import create_from_default


@pytest.mark.parametrize("spatial_dimension", [1, 2, 3, 10])
def test_optimum_value(spatial_dimension):
    """Test the optimum value; regardless of the dimension."""
    ackley_fun = create_from_default("ackley", spatial_dimension)

    xx = np.zeros((1, ackley_fun.spatial_dimension))
    yy = ackley_fun(xx)

    assert np.allclose(yy, 0.0)
