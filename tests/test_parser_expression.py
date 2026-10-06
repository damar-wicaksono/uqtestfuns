"""
Tests for the expression parser in the UQTestFuns registry.

This module contains tests for validating the parsing and resolution of
generic expressions, including literals, binary operations, and function calls.
"""

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


class TestFunctionCalls:
    """Test parsing of valid function calls."""

    @pytest.mark.parametrize(
        "expression, reference",
        [
            ("$(sqrt(4))", math.sqrt(4)),
            ("$(log(100))", math.log(100)),
            ("$(log(100, 10))", math.log(100, 10)),
            ("$(log2(8))", math.log2(8)),
            ("$(log10(1000))", math.log10(1000)),
            ("$(exp(1))", math.e),
            ("$(sin(pi/2))", math.sin(math.pi / 2)),
            ("$(cos(0))", math.cos(0)),
            ("$(tan(pi/4))", math.tan(math.pi / 4)),
            ("$(abs(-5))", abs(-5)),
        ],
        ids=[
            "sqrt",
            "log",
            "log_with_base",
            "log2",
            "log10",
            "exp",
            "sin",
            "cos",
            "tan",
            "abs",
        ],
    )
    def test_valid_expression(self, expression, reference):
        """Test parsing valid function calls with supported functions."""
        assert resolve_generic(expression) == reference

    @pytest.mark.parametrize(
        "expression",
        [
            "$(sqrt(x = 5))",  # With keyword argument
            "$(foo.bar(5))",  # Attribute access
            "$(max(*[5, 2, 1]))",  # Starred argument
            "$(max([10, 5]))",  # Unsupported function
            "$(exp(1000))",  # OverflowError
            "$(log(-5))",  # ValueError
            "$(log(1/0))",  # ZeroDivisionError
        ],
        ids=[
            "w/ keyword",
            "attribute",
            "starred",
            "unsupported",
            "overflow",
            "value_error",
            "zero_division",
        ],
    )
    def test_invalid_expression(self, expression):
        """Test parsing invalid function calls."""
        with pytest.raises(SpecValidationError):
            _ = resolve_generic(expression)
