"""
Test module specifically for UnivariateInput instances with Lognormal dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters():
    """Test the failure of specifying the parameters wrongly."""
    name = create_random_alphanumeric(5)
    distribution = "lognormal"
    # Lognormal distribution expects 2 parameters not 3!
    parameters = np.sort(np.random.rand(3))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification():
    name = create_random_alphanumeric(10)
    distribution = "lognormal"
    # The 2nd parameter of the lognormal distribution must be stricly positive!
    parameters = [7.71, -10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )
