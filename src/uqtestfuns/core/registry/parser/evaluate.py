from pathlib import Path
from typing import Optional

from uqtestfuns.core.registry.specs import CallableSpec
from .utils import parse_callable


def parse_evaluate(
    evaluate: Optional[str],
    yaml_file: Path,
    pkg_root: Path,
) -> CallableSpec:
    """Parse the evaluate section of a YAML specification.

    This function parses the 'evaluate' field from a YAML specification file
    and constructs a CallableSpec object that identifies the evaluation
    function for a UQ test function. It resolves the module path and function
    name based on the specification format, supporting both explicit and
    implicit naming conventions.

    Parameters
    ----------
    evaluate : Optional[str]
        The evaluate specification string from the YAML file. Can be:

        - None: Assumes a module file with the same name as the YAML file
          and a function named "evaluate"
        - A function name only (e.g., "my_evaluate"): Uses the specified
          function name from a module with the same name as the YAML file
        - A fully qualified path (e.g., "my_module.my_evaluate"): Uses the
          specified module file and function name
    yaml_file : Path
        Path to the YAML specification file being parsed. Used to resolve
        relative module paths when evaluate is None or partially specified.
    pkg_root : Path
        Root path of the package, used to construct the absolute module path
        relative to the package structure.

    Returns
    -------
    CallableSpec
        A specification object containing:

        - module_path: Fully qualified Python module path (dot-separated)
        - function_name: Name of the evaluation function within the module
        - kwargs: None

    Raises
    ------
    SpecValidationError
        If the specified module file does not exist or if the evaluate
        specification string is malformed (contains more than one dot).

    Notes
    -----
    - The ``module_path`` is constructed relative to the parent of ``pkg_root``
      to ensure proper Python import paths within the package structure.
    """
    if evaluate is None:
        callable_ = "evaluate"
    else:
        callable_ = evaluate

    module_path, evaluate_name = parse_callable(callable_, yaml_file, pkg_root)

    return CallableSpec(
        module_path=module_path,
        function_name=evaluate_name,
        kwargs=None,
    )
