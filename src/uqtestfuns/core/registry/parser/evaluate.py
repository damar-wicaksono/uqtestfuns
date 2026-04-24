"""Parser for the 'evaluate' section of test function YAML specification files.

This module provides functionality to parse and validate the 'evaluate' field
from YAML specification files, constructing CallableSpec objects that identify
the evaluation functions for UQ test functions.
"""

from pathlib import Path
from typing import Optional

from uqtestfuns.core.registry.specs import CallableSpec

from .utils import parse_callable


def parse_evaluate(
    evaluate_value: Optional[str],
    spec_file: Path,
    pkg_root: Path,
) -> CallableSpec:
    """Parse the 'evaluate' section of a YAML specification.

    This function parses the 'evaluate' field from a YAML specification file
    and constructs a CallableSpec object that identifies the evaluation
    function for a UQ test function. It resolves the module path and function
    name based on the specification format, supporting both explicit and
    implicit naming conventions.

    Parameters
    ----------
    evaluate_value : Optional[str]
        The value of the "evaluate" specification from the YAML file.
        This can be:

        - ``None``: Assumes a module file with the same name as the YAML file
          and a function named "evaluate"
        - A function name only (e.g., ``"my_evaluate"``): Uses the specified
          function name from a module with the same name as the YAML file
        - A fully qualified path (e.g., ``"my_module.my_evaluate"``): Uses the
          specified module file and function name
    spec_file : Path
        Path to the YAML specification file being parsed. Used to resolve
        relative module paths when evaluate is None or partially specified.
    pkg_root : Path
        Root path of the package, used to construct the absolute module path
        relative to the package structure.

    Returns
    -------
    CallableSpec
        A specification object for a callable object.

    Notes
    -----
    - The ``module_path`` is constructed relative to the parent of ``pkg_root``
      to ensure proper Python import paths within the package structure.
    """
    if evaluate_value is None:
        callable_ = "evaluate"
    else:
        callable_ = evaluate_value

    module_path, evaluate_name = parse_callable(callable_, spec_file, pkg_root)

    return CallableSpec(
        module_path=module_path,
        function_name=evaluate_name,
        kwargs=None,
    )
