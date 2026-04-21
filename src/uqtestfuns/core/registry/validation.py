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
    """Validate a marginal specification."""
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
