"""
Module for resolving YAML specification values with named constants.

This module provides functionality to resolve values from YAML specifications,
particularly handling named mathematical constants (e.g., 'pi', 'e') and
converting them to their numeric equivalents.
"""

import math

from typing import Union

from .validation import SpecValidationError

NAMED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def resolve_value(value: Union[str, float, int]) -> Union[str, float, int]:
    """Resolve a string value, substituting named constants.

    This function resolves values from YAML specifications by:
    - Returning numeric values (float, int) unchanged
    - Extracting and resolving expressions wrapped in '$()' syntax
    - Substituting named mathematical constants with their numeric values
    - Handling negative constants (e.g., '$(-pi)')

    Parameters
    ----------
    value : Union[str, float, int]
        The value to resolve.

    Returns
    -------
    Union[str, float, int]
        The resolved value. Expressions wrapped in '$()' are substituted
        with their numeric equivalents. Numeric values are returned unchanged.
        Non-expression strings are returned as-is.

    Raises
    ------
    SpecValidationError
        If the value is a string expression and cannot be evaluated.

    Notes
    -----
    - Expression syntax requires both '$(' prefix and ')' suffixes.
    - Currently, only named constants are supported for the expression.
    - Supported named constants are defined in the NAMED_CONSTANTS dictionary
    - Negative constants are handled by prefixing with '-'
      inside the expression.
    - Non-expression strings are returned unchanged (not validated).

    Examples
    --------
    >>> resolve_value(3.14)
    3.14
    >>> resolve_value("value")
    'value'
    >>> resolve_value('$(pi)')
    3.141592653589793
    >>> resolve_value('$(-pi)')
    -3.141592653589793
    >>> resolve_value('$(e)')
    2.718281828459045
    """
    if isinstance(value, str) and _is_expression(value):
        # Evaluate the expression
        value = _resolve_expression(value)

    return value


def _is_expression(value) -> bool:
    """Check if a value is an expression wrapped in '$()' syntax.

    Parameters
    ----------
    value : any
        The value to check.

    Returns
    -------
    bool
        True if the value is a string starting with '$(' and ending with ')',
        False otherwise.
    """
    if isinstance(value, str):
        return value.startswith("$(") and value.endswith(")")

    return False


def _resolve_expression(value: str) -> Union[float, int]:
    """Resolve an expression wrapped in '$()' syntax.

    This function extracts and evaluates an expression from a string value
    that is wrapped in the '$()' syntax. It supports named mathematical
    constants and their negations.

    Parameters
    ----------
    value : str
        A string expression wrapped in '$()' syntax (e.g., '$(pi)', '$(-e)').

    Returns
    -------
    Union[float, int]
        The numeric value of the resolved expression. Returns the value
        of the named constant, potentially negated if prefixed with '-'.

    Raises
    ------
    SpecValidationError
        If the expression does not match any supported named constant.

    Notes
    -----
    - The function assumes the input is already validated to have '$()' syntax.
    """
    expression = value[2:-1].strip()
    if expression.startswith("-") and expression[1:] in NAMED_CONSTANTS:
        return -1 * NAMED_CONSTANTS[expression[1:]]

    if expression in NAMED_CONSTANTS:
        return NAMED_CONSTANTS[expression]

    raise SpecValidationError(f"Unrecognized string value: {expression!r}")
