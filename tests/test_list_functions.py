"""
The test module for the high-level function 'list_functions()'
"""
import pytest

from conftest import assert_call

from uqtestfuns import list_functions, test_functions
from uqtestfuns.utils import get_available_classes, SUPPORTED_TAGS


def test_default_call():
    """Test function call without any arguments."""
    assert_call(list_functions)


@pytest.mark.parametrize("spatial_dimension", [1, 2, 10, "M"])
@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize("tabulate", [True, False, None])
def test_call_valid_arguments(spatial_dimension, tag, tabulate):
    """Test function call with valid arguments."""
    assert_call(list_functions, spatial_dimension, tag, tabulate)


@pytest.mark.parametrize("spatial_dimension", [1, -2, -3, "a"])
@pytest.mark.parametrize("tag", ["hello", "world"])
def test_call_invalid_value_arguments(spatial_dimension, tag):
    """Test function call with invalid argument values."""

    with pytest.raises(ValueError):
        list_functions(spatial_dimension, tag)


@pytest.mark.parametrize("spatial_dimension", [1, 1.0, [2], True])
@pytest.mark.parametrize("tag", ["reliability", 1.0, 5.0, False])
@pytest.mark.parametrize("tabulate", [1.0, 100, "100"])
def test_call_invalid_type_arguments(spatial_dimension, tag, tabulate):
    """Test function call with invalid argument types."""

    with pytest.raises(TypeError):
        list_functions(spatial_dimension, tag, tabulate)  # noqa


def test_untabulated_call():
    """Test function call that returns list of classes."""

    # --- Arrange
    tabulate = False

    # --- Act
    my_classes_from_list = list_functions(tabulate=tabulate)
    my_classes_ref = dict(get_available_classes(test_functions))

    # --- Assertions
    assert isinstance(my_classes_from_list, list)
    assert len(my_classes_from_list) == len(my_classes_ref)
    for my_class in my_classes_from_list:
        assert my_class in list(my_classes_ref.values())
