"""
Test module specifically for UnivariateInput instances with Gumbel (max.)
distribution.
"""
import pytest
import numpy as np

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from conftest import create_random_alphanumeric


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = "gumbel"
    # Gumbel distribution expects 2 parameters not 5!
    parameters = np.sort(np.random.rand(5))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = "gumbel"
    # The 2nd parameter of the Gumbel (max.) dist. must be strictly positive!
    parameters = [7.71, -5.0]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )
