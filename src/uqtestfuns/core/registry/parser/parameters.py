"""Parser for the parameters section in the YAML specifications.

This module provides functionality to parse and validate parameter sets
from YAML configuration files used to define UQ test function parameters.
It processes parameter specifications, resolves factory references for
dynamically created parameter values, and handles generic parameter values
including expressions.

The parser supports:
- Multiple parameter sets within a single specification
- Factory-based parameter generation using callable references
- Generic parameter values with expression resolution
- Parameter keyword descriptions for documentation
- Default parameter set selection

The main entry point is the `parse_parameters` function which returns
a ParametersVariants object containing all parsed parameter sets.
"""

from pathlib import Path
from typing import Dict

from uqtestfuns.core.registry.specs import (
    UQParametersSpec,
    ParametersVariants,
    ParametersSection,
)

from .utils import parse_factory
from .expression import resolve_generic
from .validation import SpecValidationError, validate_required_keys


def parse_parameters(
    parameters_section: ParametersSection,
    spec_file: Path,
    pkg_root: Path,
) -> ParametersVariants:
    """Parse the 'parameters' section from a YAML configuration.

    This function processes the parameter sets defined in a YAML configuration,
    resolving factory references and generic values to create structured
    parameter specifications. It validates the structure of the parameters
    section and creates UQParametersSpec objects for each parameter set.

    Parameters
    ----------
    parameters_section : ParametersSection
        Dictionary containing parameter specifications in the YAML file.
    spec_file : Path
        Path to the YAML file being parsed, used for resolving relative
        references in factory definitions and for error reporting.
    pkg_root : Path
        Root directory of the package, used for resolving module paths
        in factory definitions.

    Returns
    -------
    ParametersVariants
        Object containing a dictionary of parameter specifications by ID
        and the default parameter set ID. Each specification includes
        parameter values (either resolved generics or factory callables)
        and optional keyword descriptions.

    Raises
    ------
    SpecValidationError
        If the "sets" key is missing from parameters_value, or if any
        parameter set is not a dictionary mapping.

    Notes
    -----
    - If no default_parameters is specified in the YAML, the first parameter
      set in iteration order is used as the default.
    """
    # Check for mandatory field
    validate_required_keys(
        parameters_section,
        required_keys={"sets"},
        context=f"parameters section of {str(spec_file)}",
    )

    # Reserved keyword in "sets" section
    reserved_keywords = {"description"}

    parameters_specs: Dict[str, UQParametersSpec] = {}

    # keywords_descriptions is repeated for each specification
    keyword_descriptions = parameters_section.get("keyword_descriptions", None)

    default_id = parameters_section.get("default_parameters")

    # Iterate over available parameters sets
    parameters_sets = parameters_section["sets"]
    if default_id is None:
        default_id = next(iter(parameters_sets))
    for key, parameters_set in parameters_sets.items():
        if not isinstance(parameters_set, dict):
            raise SpecValidationError(
                f"Parameter set '{key}' must be a mapping, "
                f"got {type(parameters_set).__name__}."
            )

        parsed_values = {}
        for keyword, value in parameters_set.items():
            # Skip 'description' as a reserved key
            if keyword in reserved_keywords:
                continue
            if isinstance(value, dict) and "factory" in value:
                # Factory specification: Create a Callable ref
                parsed_values[keyword] = parse_factory(
                    value,
                    spec_file,
                    pkg_root,
                )
            else:
                # Generic value: Resolve with possible expression
                parsed_values[keyword] = resolve_generic(value)

        parameters_specs[key] = UQParametersSpec(
            name=key,
            keyword_descriptions=keyword_descriptions,
            values=parsed_values,
        )

    return ParametersVariants(
        by_id=parameters_specs,
        default_id=default_id,
    )
