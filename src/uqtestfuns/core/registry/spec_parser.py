"""YAML specification parser for test function metadata.

This module provides functionality to parse YAML specification files
that define metadata for uncertainty quantification (UQ) test functions.
It validates the structure and content of these specifications
and converts them into structured UQTestFunInfo objects.
"""

import yaml

from pathlib import Path
from typing import Callable

from .registry_entry import UQTestFunInfo, KeywordInfo


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


def parse_info(yaml_file: Path, pkg_root: Path) -> UQTestFunInfo:
    """Parse a YAML specification file and return UQTestFunInfo object.

    This function reads a YAML file containing test function metadata and
    parses it into a structured UQTestFunInfo object. It validates required
    fields and handles optional fields with default values.

    Parameters
    ----------
    yaml_file : Path
        Path to the YAML specification file containing test function metadata.
    pkg_root : Path, optional
        Root path of the package, used to resolve module paths relative to
        the package structure (default is the uqtestfuns package root).

    Returns
    -------
    UQTestFunInfo
        A structured object containing all parsed test function information,
        including name, description, tags, dimensions, inputs, and parameters.

    Raises
    ------
    KeyError
        If any mandatory field is missing from the YAML file.
    SpecValidationError
        If the spec is structurally invalid (e.g., input_dimension specified
        for a variable-dimension function, invalid field values, or empty
        inputs block).

    Notes
    -----
    Mandatory fields in the YAML file:

    - name: str
    - description: str
    - tags: list
    - variable_dimension: bool
    - inputs: dict
    - input_dimension: int (only if variable_dimension is False)
    - default_input_id: str (only if multiple inputs are defined)

    Optional fields with defaults:

    - output_dimension: int (default=1)
    - parameters: dict (default=None)
    """
    # Open the YAML file
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # --- Mandatory fields (if not specified, raise KeyError)
    name = data["name"]
    description = data["description"]
    tags = data["tags"]
    inputs = data["inputs"]

    # --- tags must be a list
    if not isinstance(tags, list):
        raise SpecValidationError(
            f"'tags' must be a list, "
            f"got {type(tags).__name__!r} in {yaml_file}"
        )

    # --- Input dimension (conditionally optional)
    dimensions = data["dimensions"]
    input_dimension = dimensions["input"]
    if input_dimension == "variable":
        variable_dimension = True
        input_dimension = None
    else:
        if not isinstance(input_dimension, int) or input_dimension < 1:
            raise SpecValidationError(
                f"'input_dimension' must be a positive integer, "
                f"got {input_dimension!r} in {yaml_file}"
            )
        variable_dimension = False

    # --- Output dimension (optional with default value)
    output_dimension = dimensions.get("output_dimension", 1)

    # --- File references
    spec_path = yaml_file.resolve()

    # --- Inputs specification
    if not inputs:
        raise SpecValidationError(
            f"'inputs' must contain at least one entry in {yaml_file}"
        )
    available_input_ids = {k: v.get("description") for k, v in inputs.items()}
    if len(inputs) == 1:
        default_input_id = next(iter(inputs))
    else:
        default_input_id = data["default_input"]

    # --- Parameter specification (optional; None if not defined)
    parameters = data.get("parameters")
    if parameters is None:
        available_parameter_ids = None
        default_parameter_id = None
        parameter_keywords = None
    else:
        # -- Validate that 'sets' sub-block is present and non-empty
        available_sets = parameters.get("sets")
        if not available_sets:
            raise SpecValidationError(
                f"'parameters' block is present but missing 'sets' "
                f"in {yaml_file}"
            )

        # -- Collect available parameter set IDs and their descriptions
        keyword_descriptions = parameters.get("keywords", {})
        available_parameter_ids = {
            k: v.get("description") for k, v in available_sets.items()
        }

        # -- Resolve default parameter set ID
        if len(available_sets) == 1:
            default_parameter_id = next(iter(available_sets))
        else:
            default_parameter_id = parameters["default_parameters"]

        # -- Infer keyword types from the default parameter set
        default_set = available_sets[default_parameter_id]
        default_set = {
            k: v for k, v in default_set.items() if k != "description"
        }
        parameter_keywords = {}
        for k, v in default_set.items():
            is_callable = isinstance(v, str) and v.endswith("()")
            parameter_keywords[k] = KeywordInfo(
                type=Callable if is_callable else type(v),
                description=keyword_descriptions.get(k),
            )

    return UQTestFunInfo(
        name,
        description,
        tags,
        variable_dimension,
        input_dimension,
        output_dimension,
        spec_path,
        available_input_ids,
        default_input_id,
        available_parameter_ids,
        default_parameter_id,
        parameter_keywords,
    )
