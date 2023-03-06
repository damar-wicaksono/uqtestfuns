"""
Test module for the Sulfur model test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""
import numpy as np

from uqtestfuns import Sulfur
from uqtestfuns.test_functions import sulfur as sulfur_mod


def _compute_sqrt_geometric_mean_std(marginals):
    """Compute the sqrt. geom. mean and std. deviation of the Sulfur model."""

    # Compute the mean and std. of the underlying normal distribution
    mu = 0.0
    var = 0.0
    for i in range(9):
        mu += marginals[i].parameters[0]
        var += marginals[i].parameters[1] ** 2

    # Plus some additional factors in the Sulfur model formula (only for mu)
    solar_constant = sulfur_mod.SOLAR_CONSTANT
    earth_area = sulfur_mod.EARTH_AREA
    days_in_year = sulfur_mod.DAYS_IN_YEAR
    mu += (
        np.log(1e12)
        + np.log(0.5)
        + np.log(3)
        + np.log(solar_constant)
        - np.log(earth_area)
        - np.log(days_in_year)
    )

    # Get the standard deviation
    sigma = np.sqrt(var)

    return mu, sigma


def test_compute_mean():
    """Test the mean computation as the result is analytical."""

    # Create an instance of Sulfur model
    my_fun = Sulfur()

    # Assert that ProbInput is correctly attached
    assert my_fun.prob_input is not None

    # Compute mean via Monte Carlo
    xx = my_fun.prob_input.get_sample(1000000)
    yy = my_fun(xx)

    mean_mc = np.mean(np.log(-1 * yy))

    # Analytical mean
    marginals = my_fun.prob_input.marginals
    mean_ref = _compute_sqrt_geometric_mean_std(marginals)[0]

    # Assertion
    assert np.allclose(mean_mc, mean_ref, rtol=1e-1)


def test_compute_std():
    """Test the standard deviation computation as the result is analytical."""

    # Create an instance of Sulfur model
    my_fun = Sulfur()

    # Assert that ProbInput is correctly attached
    assert my_fun.prob_input is not None

    # Compute mean via Monte Carlo
    xx = my_fun.prob_input.get_sample(1000000)
    yy = my_fun(xx)

    std_mc = np.std(np.log(-1 * yy))

    # Analytical standard deviation
    marginals = my_fun.prob_input.marginals
    std_ref = _compute_sqrt_geometric_mean_std(marginals)[1]

    # Assertion
    assert np.allclose(std_mc, std_ref, rtol=1e-1)
