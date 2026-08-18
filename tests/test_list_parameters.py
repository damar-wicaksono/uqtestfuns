"""
The test module for the high-level function 'list_parameters()'
"""

from conftest import assert_call

from uqtestfuns.api import create, list_functions, list_parameters
from uqtestfuns.core.registry import get_registry


def test_default_call():
    """Test function call without any arguments."""
    list_names = list_functions(tabulate=False)
    for name in list_names:  # type: ignore
        assert_call(list_parameters, name)


def test_create_function():
    """Test creating a function with parameter IDs supplied by the function."""
    list_names = list_functions(tabulate=False)
    reg = get_registry()
    for name in list_names:  # type: ignore
        param_ids = list_parameters(name, tabulate=False)
        for param_id in param_ids:
            if reg[name].input_dimension is None:
                assert_call(create, name, 2, parameters_id=param_id)
            else:
                assert_call(create, name, parameters_id=param_id)


def test_no_parameter():
    """Test listing parameters when no parameter is available."""
    function_names = list_functions(parameterized=False, tabulate=False)
    for function_name in function_names:  # type: ignore
        param_ids = list_parameters(function_name, tabulate=False)

        # Assertion
        assert len(param_ids) == 0


def test_with_parameter():
    """Test listing parameters when one or more parameter is available."""
    function_names = list_functions(parameterized=True, tabulate=False)
    for function_name in function_names:  # type: ignore
        param_ids = list_parameters(function_name, tabulate=False)

        # Assertion
        assert len(param_ids) > 0
