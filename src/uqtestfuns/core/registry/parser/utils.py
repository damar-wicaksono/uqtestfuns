import yaml

from pathlib import Path


def safe_load(yaml_file: Path) -> dict:
    """Load and parse a YAML file using safe loading.

    This helper function reads a YAML specification file and parses it
    into a Python dictionary using PyYAML's safe_load method, which
    prevents arbitrary code execution and only constructs simple Python
    objects (strings, lists, dicts, numbers, dates, etc.).

    Parameters
    ----------
    yaml_file : Path
        Path to the YAML file to be loaded.

    Returns
    -------
    dict
        Parsed YAML content as a Python dictionary containing the
        specification data.

    Notes
    -----
    - This function uses `yaml.safe_load()` rather than `yaml.load()` to
      ensure security by preventing the execution of arbitrary Python code
      that might be embedded in malicious YAML files.
    """
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    return data


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


def resolve_generic(value: Union[str, float, int]) -> Union[str, float, int]:
    """Resolve generic value to either numeric or string value.

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
    >>> resolve_yaml_val(3.14)
    3.14
    >>> resolve_yaml_val("value")
    'value'
    >>> resolve_yaml_val('$(pi)')
    3.141592653589793
    >>> resolve_yaml_val('$(-pi)')
    -3.141592653589793
    >>> resolve_yaml_val('$(e)')
    2.718281828459045
    """
    if isinstance(value, str) and _is_expression(value):
        # Evaluate the expression
        value = _resolve_expression(value)

    return value


def resolve_numeric(value: Union[str, float, int]) -> Union[float, int]:
    """Resolve a value to a numeric type.

    Parameters
    ----------
    value : Union[str, float, int]
        The value to resolve. Can be a numeric value or a string expression.

    Returns
    -------
    Union[float, int]
        The resolved numeric value.

    Raises
    ------
    SpecValidationError
        If the value is a string that is not a valid expression.
    """
    if isinstance(value, (float, int)):
        return value

    if not _is_expression(value):
        raise SpecValidationError(
            f"Unrecognized string value: {value!r}, "
            f"numeric value is expected."
        )

    return _resolve_expression(value)


def _is_expression(value: Union[str, float, int]) -> bool:
    """Check if a value is an expression wrapped in '$()' syntax.

    Parameters
    ----------
    value : Union[str, float, int]
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

    # Handle negative constants
    is_negative = expression.startswith("-")
    constant_name = expression[1:] if is_negative else expression

    if constant_name in NAMED_CONSTANTS:
        result = NAMED_CONSTANTS[constant_name]
        return -result if is_negative else result

    raise SpecValidationError(f"Unrecognized string value: {expression!r}")
