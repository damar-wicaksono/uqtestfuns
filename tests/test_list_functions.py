"""
The test module for the high-level function 'list_functions()'
"""

import pytest

from conftest import assert_call

from uqtestfuns.api import create, list_functions
from uqtestfuns.core.registry import get_registry
from uqtestfuns.global_settings import SUPPORTED_TAGS


def test_default_call():
    """Test function call without any arguments."""
    assert_call(list_functions)


class TestValidArgument:
    """A series of tests for calling list_functions() with valid arguments."""

    @pytest.mark.parametrize("input_dimension", [1, 2, 10, "M", None])
    def test_input_dimension(self, input_dimension):
        """Test function call with an 'input_dimension' argument."""
        assert_call(list_functions, input_dimension=input_dimension)

    @pytest.mark.parametrize("tag", SUPPORTED_TAGS)
    def test_tag(self, tag):
        """Test function call with a 'tag' argument."""
        assert_call(list_functions, tag=tag)

    @pytest.mark.parametrize("output_dimension", [1, 2, 3, None])
    def test_output_dimension(self, output_dimension):
        """Test function call with an 'output_dimension' argument."""
        assert_call(list_functions, output_dimension=output_dimension)

    @pytest.mark.parametrize("parameterized", [True, False, None])
    def test_parameterized(self, parameterized):
        """Test function call with a 'parameterized' argument."""
        assert_call(list_functions, parameterized=parameterized)

    @pytest.mark.parametrize("tabulate", [True, False, None])
    def test_tabulate(self, tabulate):
        """Test function call with a 'tabulate' argument."""
        assert_call(list_functions, tabulate=tabulate)


class TestInvalidValueArgument:
    """A series of tests for calling list_functions() w/ invalid value arg."""

    @pytest.mark.parametrize("input_dimension", [-1, -2, -3, "a"])
    def test_input_dimension(self, input_dimension):
        """Test function call with an invalid value for 'input_dimension'."""
        with pytest.raises(ValueError):
            list_functions(input_dimension=input_dimension)

    @pytest.mark.parametrize("tag", ["hello", "world"])
    def test_tag(self, tag):
        """Test function call with an invalid value for 'tag'."""
        with pytest.raises(ValueError):
            list_functions(tag=tag)

    @pytest.mark.parametrize("output_dimension", [-1, -2, -3])
    def test_output_dimension(self, output_dimension):
        """Test function call with an invalid value for 'output_dimension'."""
        with pytest.raises(ValueError):
            list_functions(output_dimension=output_dimension)


class TestInvalidTypeArgument:
    """A series of tests for calling list_functions() w/ invalid type arg."""

    @pytest.mark.parametrize("input_dimension", [1.0, [2]])
    def test_input_dimension(self, input_dimension):
        """Test function call with an invalid type for 'input_dimension'."""
        with pytest.raises(TypeError):
            list_functions(input_dimension=input_dimension)

    @pytest.mark.parametrize("tag", [1.0, 5.0, False])
    def test_tag(self, tag):
        """Test function call with an invalid type for 'tag'."""
        with pytest.raises(TypeError):
            list_functions(tag=tag)

    @pytest.mark.parametrize("output_dimension", ["a", [2]])
    def test_output_dimension(self, output_dimension):
        """Test function call with an invalid type for 'output_dimension'."""
        with pytest.raises(TypeError):
            list_functions(output_dimension=output_dimension)

    @pytest.mark.parametrize("parameterized", ["a", 1, 2])
    def test_parameterized(self, parameterized):
        """Test function call with an invalid type for 'parameterized'."""
        with pytest.raises(TypeError):
            list_functions(parameterized=parameterized)

    @pytest.mark.parametrize("tabulate", [1.0, 100, "100"])
    def test_tabulate(self, tabulate):
        """Test function call with an invalid type for 'tabulate'."""
        with pytest.raises(TypeError):
            list_functions(tabulate=tabulate)


def test_untabulated_call():
    """Test function call that returns a list of keys in the registry."""

    # --- Arrange
    tabulate = False
    reg = get_registry()

    # --- Act
    my_classes_from_list = list_functions(tabulate=tabulate)

    # --- Assertions
    # The output is a list
    assert isinstance(my_classes_from_list, list)
    # Consistent length with the registry
    assert len(my_classes_from_list) == len(reg)
    for my_class in my_classes_from_list:
        # The key is in the registry
        assert my_class in reg
        # The corresponding test function can be created
        if reg[my_class].input_dimension is None:
            assert_call(create, my_class, 2)
        else:
            assert_call(create, my_class)


def test_tablefmt_html():
    """Test function call with 'html' as tablefmt."""

    table = list_functions(tablefmt="html")

    # Assertion
    assert isinstance(table, str)
