"""
Test module for the Grammacy1DSine test function.

Notes
-----
- The tests defined in this module deals with
  the correctness of the evaluation.
"""

import pytest

from uqtestfuns import Gramacy1DSine
import uqtestfuns.test_functions.gramacy2007 as gramacy_mod

from conftest import assert_call

# Test for different parameters to the Ishigami function
available_parameters = list(Gramacy1DSine.available_parameters.keys())


@pytest.fixture(params=available_parameters)
def gramacy1dsine_fun(request):
    gramacy1dsine = Gramacy1DSine(parameters_selection=request.param)

    return gramacy1dsine


@pytest.mark.parametrize("param_selection", available_parameters)
def test_different_parameters(param_selection):
    """Test selecting different built-in parameters."""

    # Create an instance of Ishigami function with a specified param. selection
    my_testfun = Gramacy1DSine(parameters_selection=param_selection)

    # Assertion
    assert (
        my_testfun.parameters
        == gramacy_mod.AVAILABLE_PARAMETERS[param_selection]
    )

    # Assert Call
    xx = my_testfun.prob_input.get_sample(10)
    assert_call(my_testfun, xx)


def test_wrong_param_selection():
    """Test a wrong selection of the parameters."""
    with pytest.raises(KeyError):
        Gramacy1DSine(parameters_selection="marelli1")
