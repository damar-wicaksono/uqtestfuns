import re


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

    pass


def validate_marginal(marginal: dict) -> None:
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
    errors = []

    # --- Mandatory keys
    required_keys = {"distribution", "parameters"}
    missing_keys = required_keys - marginal.keys()
    if missing_keys:
        errors.append(f"Missing mandatory keys: {missing_keys}")

    # --- Extraneous keys
    supported_keys = {"distribution", "parameters", "name", "description"}
    extra_keys = marginal.keys() - supported_keys
    if extra_keys:
        errors.append(f"Unexpected keys: {extra_keys}")

    if errors:
        raise SpecValidationError(
            f"Invalid marginal {marginal}: " + "; ".join(errors)
        )


def validate_callable_string(callable_: str) -> None:
    """Validate a callable string specification.

    This function validates that a callable string follows the expected format
    for referencing Python callables in YAML specifications.
    Valid formats are:

    - ``name``: a simple callable name (e.g., function or class)
    - ``module.name``: a module-qualified callable name

    Parameters
    ----------
    callable_ : str
        The callable string to validate. Must be in the format ``name`` or
        ``module.name``, where ``name`` and ``module`` contain only
        alphanumeric characters and underscores.

    Raises
    ------
    SpecValidationError
        If the callable string does not match the expected format, or if it
        contains more than one dot (nested modules are not supported).
    """
    pattern = re.compile(r"^([A-Za-z0-9_]+\.)?[A-Za-z0-9_]+$")

    if not pattern.fullmatch(callable_):
        raise SpecValidationError(
            f"Invalid callable specification {callable_!r}: "
            "expected 'name' or 'module.name', got "
            f"{len(callable_.split('.')) - 1} dots"
        )
