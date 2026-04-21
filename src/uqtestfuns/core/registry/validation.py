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
