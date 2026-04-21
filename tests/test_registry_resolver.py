"""
Test module for value resolution functionality in the registry resolver.
"""

import math
import pytest

from uqtestfuns.core.registry.validation import SpecValidationError
from uqtestfuns.core.registry.resolver import resolve_value

SUPPORTED_CONSTANTS = ["pi", "e"]


class TestResolveValue:
    """All tests related to resolving values."""

    @pytest.mark.parametrize("value", [1.0, 2, "1", "abc"])
    def test_numerical_values(self, value):
        """Test resolving non-expression values; return as-is."""

        # Resolve value
        value_ = resolve_value(value)

        # Assertions
        assert value_ == value
        assert value_ is value

    @pytest.mark.parametrize("value", SUPPORTED_CONSTANTS)
    def test_supported_constants(self, value):
        """Test resolving supported constants."""

        # Create an expression
        expr = f"$( {value} )"

        # Resolve value
        value_ = resolve_value(expr)

        # Assertion
        assert value_ == getattr(math, value)

    @pytest.mark.parametrize("value", SUPPORTED_CONSTANTS)
    def test_negation(self, value):
        """Test resolving the negation of supported constants."""

        # Create an expression
        expr = f"$( -{value} )"

        # Resolve value
        value_ = resolve_value(expr)

        # Assertion
        assert value_ == -getattr(math, value)

    @pytest.mark.parametrize("value", ["a", "b", "c"])
    def test_unsupported_constants(self, value):
        """Test resolving unsupported constants."""

        # Create an expression
        expr = f"$( {value} )"

        # Assertion
        with pytest.raises(SpecValidationError):
            _ = resolve_value(expr)

    def test_empty_expression(self):
        """Test resolving an empty expression."""

        # Create an expression
        expr = "$()"

        # Assertion
        with pytest.raises(SpecValidationError):
            _ = resolve_value(expr)
