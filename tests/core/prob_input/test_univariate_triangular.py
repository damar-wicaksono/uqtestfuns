"""
Test module specifically for UnivariateInput instances with triangular dist.
"""

import pytest
import numpy as np

from uqtestfuns.core.prob_input.marginal import Marginal
from conftest import create_random_alphanumeric

DISTRIBUTION_NAME = "triangular"


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    # A triangular distribution expects 3 parameters not 10!
    parameters = np.sort(np.random.rand(10))

    with pytest.raises(ValueError):
        Marginal(
            name=name, distribution=DISTRIBUTION_NAME, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    # The lower bound must be smaller than the upper bound!
    parameters = [5, 1, 3]

    with pytest.raises(ValueError):
        Marginal(
            name=name, distribution=DISTRIBUTION_NAME, parameters=parameters
        )

    # The mid-point value must be between lower and upper bounds!
    parameters = [3, 4, 10]

    with pytest.raises(ValueError):
        Marginal(
            name=name, distribution=DISTRIBUTION_NAME, parameters=parameters
        )


def test_estimate_mode() -> None:
    """Test the mode estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(3))
    parameters[[2, 1]] = parameters[[1, 2]]

    # Create an instance
    my_univariate_input = Marginal(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-0 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    y, edges = np.histogram(xx, bins="auto")
    mode = edges[np.argmax(y)]

    # Analytical result
    mode_ref = parameters[2]

    # Assertion
    assert np.isclose(mode, mode_ref, rtol=1, atol=1)
