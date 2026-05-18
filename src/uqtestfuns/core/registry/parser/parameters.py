"""Parser for the parameters section in the YAML specifications.

This module provides functionality to parse and validate parameter sets
from YAML configuration files. It processes parameter specifications,
resolves factory references for dynamically created parameter values,
and handles generic parameter values including expressions.
"""

from pathlib import Path
from typing import Any, Dict

from uqtestfuns.core.registry.specs import UQParametersSpec

from .utils import parse_factory
from .expression import resolve_generic
from .validation import SpecValidationError, validate_required_keys


def parse_parameters(
    parameters_value: Dict[str, Dict[str, Any]],
    spec_file: Path,
    pkg_root: Path,
) -> Dict[str, UQParametersSpec]:
    """Parse the 'parameters' section from a YAML configuration.

    This function processes the parameter sets defined in a YAML configuration,
    resolving factory references and generic values to create structured
    parameter specifications.

    Parameters
    ----------
    parameters_value : Dict[str, Any]
        Dictionary containing parameter sets under a "sets" key. Each set
        contains keyword-value pairs defining parameters.
    spec_file : Path
        Path to the YAML file being parsed, used for resolving relative
        references in factory definitions.
    pkg_root : Path
        Root directory of the package, used for resolving module paths
        in factory definitions.

    Returns
    -------
    Dict[str, UQParametersSpec]
        Dictionary mapping parameter set names to their corresponding
        UQParametersSpec objects, which contain parameter descriptions
        and parsed values.
    """
    # Check for mandatory field
    validate_required_keys(
        parameters_value,
        required_keys={"sets"},
        context=f"parameters section of {str(spec_file)}",
    )

    # Reserved keyword in "sets" section
    reserved_keywords = {"description"}

    parameters_specs: Dict[str, UQParametersSpec] = {}

    # keywords_descriptions is repeated for each specification
    keyword_descriptions = parameters_value.get("keyword_descriptions", None)

    # Iterate over available parameters sets
    parameters_sets = parameters_value["sets"]
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

    return parameters_specs
