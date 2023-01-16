"""
Test module specifically for UnivariateInput instances with triangular dist.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = "triangular"
    # Normal distribution expects 3 parameters not 10!
    parameters = np.sort(np.random.rand(10))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = "triangular"
    # The lower bound must be smaller than the upper bound!
    parameters = [5, 1, 3]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The mid-point value must be between lower and upper bounds!
    parameters = [3, 4, 10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )
