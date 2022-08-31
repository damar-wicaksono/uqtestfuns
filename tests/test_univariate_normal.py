"""
Test module specifically for UnivariateInput instances with normal dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters():
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = "normal"
    # Normal distribution expects 2 parameters not 10!
    parameters = np.sort(np.random.rand(10))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification():
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = "normal"
    # The 2nd parameter of the normal distribution must be stricly positive!
    parameters = [7.71, -1]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )
