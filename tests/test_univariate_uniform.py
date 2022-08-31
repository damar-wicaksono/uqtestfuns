"""
Test module specifically for UnivariateInput instances with uniform dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_parameters():
    """Test the failure of specifying the parameters wrongly."""
    name = create_random_alphanumeric(5)
    distribution = "uniform"
    # Uniform distribution expects 2 parameters not 1!
    parameters = np.sort(np.random.rand(1))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification():
    name = create_random_alphanumeric(10)
    distribution = "uniform"
    # The lower bound must be smaller than upper bound!
    parameters = [10, -10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )