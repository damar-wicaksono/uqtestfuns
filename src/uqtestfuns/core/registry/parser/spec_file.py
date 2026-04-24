from pathlib import Path

from uqtestfuns.core.registry.registry_entry import UQTestFunSpec

from .evaluate import parse_evaluate
from .inputs import parse_inputs
from .parameters import parse_parameters
from .validation import SpecValidationError, validate_required_keys
from .utils import safe_load

__all__ = ["parse_spec"]


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
    evaluate = parse_evaluate(
        data.get("evaluate", None),
        spec_file,
        pkg_root,
    )

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
