from pathlib import Path
from typing import Callable, Dict

import yaml

from uqtestfuns.core.registry.entries import (
    UQTestFunInfo,
    UQTestFunSpec,
    KeywordInfo,
)
from .evaluate import parse_evaluate
from .inputs import parse_inputs
from .parameters import parse_parameters
from .utils import safe_load
from .validation import SpecValidationError, validate_required_keys

__all__ = ["parse_info", "parse_spec"]


def parse_info(yaml_file: Path) -> UQTestFunInfo:
    """Parse a YAML specification file and return UQTestFunInfo object.

    This function reads a YAML file containing test function metadata and
    parses it into a structured UQTestFunInfo object. It validates required
    fields and handles optional fields with default values.

    Parameters
    ----------
    yaml_file : Path
        Path to the YAML specification file containing test function metadata.

    Returns
    -------
    UQTestFunInfo
        A structured object containing all parsed test function information,
        including name, description, tags, dimensions, inputs, and parameters.

    Raises
    ------
    SpecValidationError
        If the spec is missing obligatory fields/keys and/or structurally
        invalid (e.g., input_dimension specified for a variable-dimension
        function, invalid field values, or empty inputs block).

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
    required_keys = {"name", "description", "tags", "inputs", "dimensions"}
    validate_required_keys(data, required_keys, str(yaml_file))

    # --- Get the name and description
    name = data["name"]
    description = data["description"]

    # --- tags must be a list
    tags = data["tags"]
    if not isinstance(tags, list):
        raise SpecValidationError(
            f"'tags' must be a list, "
            f"got {type(tags).__name__!r} in {yaml_file}"
        )

    # --- Input dimension
    dimensions = data["dimensions"]
    input_dimension = dimensions["input"]
    if input_dimension == "variable":
        input_dimension = None
    else:
        if not isinstance(input_dimension, int) or input_dimension < 1:
            raise SpecValidationError(
                f"'input_dimension' must be a positive integer, "
                f"got {input_dimension!r} in {yaml_file}"
            )

    # --- Output dimension (optional with default value)
    output_dimension = dimensions.get("output_dimension", 1)

    # --- File references
    spec_path = yaml_file.resolve()

    # --- Inputs specification
    inputs = data["inputs"]
    if not inputs:
        raise SpecValidationError(
            f"'inputs' must contain at least one entry in {yaml_file}"
        )
    if isinstance(inputs, str):
        # Specification in a separate file
        inputs_yaml = yaml_file.resolve().with_name(inputs)
        inputs = safe_load(inputs_yaml)

    available_input_ids = {k: v.get("description") for k, v in inputs.items()}
    if len(inputs) == 1:
        default_input_id = next(iter(inputs))
    else:
        default_input_id = data["default_input"]

    # --- Parameter specification (optional; None if not defined)
    parameters = data.get("parameters")
    parameters_keywords: Dict[str, Dict[str, KeywordInfo]] = {}
    if parameters is None:
        available_parameter_ids = {}
        default_parameter_id = None
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

        # -- Infer keyword types from each of the available sets
        for set_name, available_set in available_sets.items():
            # Filter it
            available_set = {
                k: v for k, v in available_set.items() if k != "description"
            }
            parameters_keywords[set_name] = {}
            for k, v in available_set.items():
                is_callable = isinstance(v, dict) and "factory" in v
                parameters_keywords[set_name][k] = KeywordInfo(
                    type=Callable if is_callable else type(v),
                    description=keyword_descriptions.get(k),
                )

    return UQTestFunInfo(
        name,
        description,
        tags,
        input_dimension,
        output_dimension,
        spec_path,
        available_input_ids,
        default_input_id,
        available_parameter_ids,
        default_parameter_id,
        parameters_keywords,
    )


def parse_spec(spec_file: Path, pkg_root: Path) -> UQTestFunSpec:
    """Parse a specification file and return the UQTestFunSpec object.

    UQTestFunSpec contains all the information required to instantiate UQ
    test function. It belongs to the instantiation layer of the registry
    system.

    Parameters
    ----------
    spec_file : Path
        Path to the YAML specification file containing test function metadata.
    pkg_root : Path
        Root path of the package, used to resolve module paths relative to
        the package structure.

    Returns
    -------
    UQTestFunSpec
        A structured object containing all parsed test function specifications
        required for instantiation, including name, evaluate callable,
        input specifications, and parameter specifications.

    Raises
    ------
    SpecValidationError
        If the spec is structurally invalid (e.g., invalid field values,
        missing module files, or malformed specification blocks).

    Notes
    -----
    This function parses the complete specification needed to instantiate
    a UQ test function, including:

    - evaluate: CallableSpec defining the evaluation function
    - inputs: Dictionary of UQInputSpec objects defining input distributions
    - parameters: Dictionary of UQParameterSpec objects (optional)

    Unlike `parse_info()` which extracts metadata for discovery purposes,
    this function parses the full specification required for instantiation.
    """
    # Read the specification (YAML) file
    data = safe_load(spec_file)

    # YAML file cannot be empty
    if not isinstance(data, dict):
        raise SpecValidationError(f"Invalid YAML structure in {spec_file}")

    # Check mandatory fields in spec parsing context
    validate_required_keys(data, {"name", "inputs"}, str(spec_file))

    # Get the name
    name = data["name"]

    # Parse the "evaluate" section and return a CallableSpec
    evaluate = parse_evaluate(data.get("evaluate"), spec_file, pkg_root)

    # Parse the "inputs" section and return a dictionary of UQInputSpec
    inputs = parse_inputs(data["inputs"], spec_file, pkg_root)

    # Parse the "parameters" section & return a dictionary of UQParametersSpec
    if "parameters" not in data:
        parameters = None
    else:
        parameters = parse_parameters(data["parameters"], spec_file, pkg_root)

    return UQTestFunSpec(
        name=name,
        evaluate=evaluate,
        inputs=inputs,
        parameters=parameters,
    )
