"""Validation utilities for YAML specification parsing.

This module provides validation functions for YAML specification files used
in the UQTestFuns registry system. It includes validators for marginal
distributions, callable string references, and general dictionary structure
validation with required keys.
"""

import re

from typing import Any, Dict, Iterable


class SpecValidationError(Exception):
    """Exception raised when YAML specification validation fails.

    This exception is raised when a YAML specification file contains
    structural or semantic errors, such as:

    - Invalid field types or values
    - Conflicting configuration (e.g., input_dimension specified for
      variable-dimension functions)
    - Empty required blocks (e.g., inputs or parameter sets)

    It is used throughout the spec_parser module to provide clear error
    messages about specification validation failures.
    """


def validate_marginal(marginal: Dict[str, Any]) -> None:
    """Validate a marginal specification.

    Checks that the marginal dictionary contains required keys
    (``'distribution'`` and ``'parameters'``) and only supported optional keys
    (``'name'`` and ``'description'``).

    Parameters
    ----------
    marginal : dict
        The marginal specification dictionary to validate.

    Raises
    ------
    SpecValidationError
        If required keys are missing or unsupported keys are present.
    """
    # --- Mandatory keys
    required_keys = {"distribution", "parameters"}
    validate_required_keys(marginal, required_keys, context="marginal")

    # --- Extraneous keys
    supported_keys = {"distribution", "parameters", "name", "description"}
    extra_keys = marginal.keys() - supported_keys
    if extra_keys:
        raise SpecValidationError(
            f"Unexpected keys: {extra_keys} in {marginal}"
        )


def validate_callable_string(callable_string: str) -> None:
    """Validate a callable string specification.

    This function validates that a callable string follows the expected format
    for referencing Python callables in the YAML specifications.

    Valid formats are:

    - ``name``: a simple callable name
    - ``module.name``: a module-qualified callable name

    Each segment must be a valid Python identifier, and nested modules are
    not supported.

    Parameters
    ----------
    callable_string : str
        The callable string to validate.

    Raises
    ------
    SpecValidationError
        If the callable string does not match the expected format.
    """
    # Match pattern '[module.]name' and
    # 'module' and 'name' are valid Python identifiers
    valid_pattern = re.compile(r"^([A-Za-z_]\w*\.)?[A-Za-z_]\w*$")

    # Match Python valid identifier
    if not valid_pattern.fullmatch(callable_string):
        raise SpecValidationError(
            f"Invalid callable specification {callable_string!r}: "
            "expected 'name' or 'module.name' using valid Python identifiers"
        )


def validate_required_keys(
    data: dict,
    required_keys: Iterable[str],
    context: str,
) -> None:
    """Validate that all required keys are present in a dictionary.

    This function checks that a dictionary contains all mandatory keys
    specified in the required_keys parameter. If any keys are missing,
    it raises a SpecValidationError with a descriptive message indicating
    which fields are missing and in what context.

    Parameters
    ----------
    data : dict
        The dictionary to validate.
    required_keys : Iterable[str]
        An iterable of key names that must be present in the dictionary.
    context : str
        A description of the context being validated (e.g., "marginal",
        "input specification"), used in error messages.

    Raises
    ------
    SpecValidationError
        If any required keys are missing from the dictionary.
    """
    missing_keys = sorted(set(required_keys) - set(data.keys()))
    if missing_keys:
        raise SpecValidationError(
            f"Missing mandatory fields in {context}: {', '.join(missing_keys)}"
        )
