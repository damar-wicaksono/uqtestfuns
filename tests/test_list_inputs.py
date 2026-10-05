"""
The test module for the high-level function 'list_inputs()'
"""

from conftest import assert_call

from uqtestfuns.api import create, list_functions, list_inputs
from uqtestfuns.core.registry import get_registry


def test_default_call():
    """Test function call without any arguments."""
    list_names = list_functions(tabulate=False)
    for name in list_names:
        assert_call(list_inputs, name)


def test_create_function():
    """Test creating a function with inputs IDs supplied by the function."""
    list_names = list_functions(tabulate=False)
    reg = get_registry()
    for name in list_names:
        input_ids = list_inputs(name, tabulate=False)
        for input_id in input_ids:
            if reg[name].variable_dimension:
                assert_call(create, name, 2, input_id=input_id)
            else:
                assert_call(create, name, input_id=input_id)


def test_number_of_specification():
    """Test at least one specification is available."""
    function_names = list_functions(tabulate=False)
    for function_name in function_names:
        input_ids = list_inputs(function_name, tabulate=False)

        # Assertion
        assert len(input_ids) > 0
