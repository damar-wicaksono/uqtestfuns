import math
import pytest

from uqtestfuns.core.registry.parser.expression import resolve_generic
from uqtestfuns.core.registry.parser.validation import SpecValidationError


@pytest.mark.parametrize(
    "invalid_expression",
    [
        "$(x = 5)",  # Assignment
        "$('foo')",  # String literal
        "$(True)",  # Boolean literal
        "$(5 // 2)",  # Integer division
        "$(5 / 0)",  # Division by zero
        "$(5 == 5)",  # Compare expression
    ],
)
def test_invalid_expression(invalid_expression):
    """Test parsing of invalid expression syntax."""
    with pytest.raises(SpecValidationError):
        _ = resolve_generic(invalid_expression)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("$(5)", 5),
        ("$(3.14)", 3.14),
        ("$(-5)", -5),
        ("$(+5)", 5),
    ],
)
def test_valid_literal(input_value, expected_value):
    """Test parsing of valid literal expressions."""
    resolved = resolve_generic(input_value)

    # Assertion
    assert resolved == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("$(1 / 3)", 1 / 3),
        ("$(2**3)", 2**3),
        ("$(2-3)", 2 - 3),
        ("$(2 * (pi + 5))", 2 * (math.pi + 5)),
        ("$(2 * (pi + (5 - 4)))", 2 * (math.pi + 1)),
    ],
)
def test_valid_binary_op(input_value, expected_value):
    """Test parsing of valid binary operations."""
    resolved = resolve_generic(input_value)

    # Assertion
    assert resolved == expected_value
