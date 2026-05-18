import pytest

from uqtestfuns.core.registry.parser.expression import resolve_generic
from uqtestfuns.core.registry.parser.validation import SpecValidationError


@pytest.mark.parametrize(
    "invalid_expression", ["$(x = 5)", "$('foo')", "$(True)", "$(5 * pi)"]
)
def test_invalid_expression(invalid_expression):
    """Test parsing of invalid expression syntax."""
    with pytest.raises(SpecValidationError):
        _ = resolve_generic(invalid_expression)


@pytest.mark.parametrize(
    "input_value, expected_value", [("$(5)", 5), ("$(3.14)", 3.14)]
)
def test_valid_literal(input_value, expected_value):
    """Test parsing of valid literal expressions."""
    resolved = resolve_generic(input_value)

    # Assertion
    assert resolved == expected_value
