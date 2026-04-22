from pathlib import Path
from typing import Optional, Tuple

from uqtestfuns.core.registry.specs import CallableSpec

from .validation import validate_callable_string, SpecValidationError


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


def parse_callable(
    callable_: str,
    yaml_file: Path,
    pkg_root: Path,
) -> Tuple[str, str]:
    """Parse a callable spec string into the module path and the function name.

    This helper function parses a callable specification string (typically from
    a YAML file) and resolves it into a fully qualified Python module path and
    a function name. It supports both explicit ``module.function`` notation and
    implicit module resolution based on the YAML file name.

    Parameters
    ----------
    callable_ : str
        The callable specification string. The possible values are:

        - A function name only (e.g., ``my_function``): Uses the specified
          function name from a module with the same name as the YAML file
        - A fully qualified path (e.g., ``my_module.my_function``): Uses the
          specified module file and function name
    yaml_file : Path
        Path to the YAML specification file. Used to resolve relative module
        paths when the value contains only a function name.
    pkg_root : Path
        Root path of the package, used to construct the absolute module path
        relative to the package structure.

    Returns
    -------
    Tuple[str, str]
        A tuple of strings containing:

        - ``module_path``: Fully qualified Python module path (dot-separated)
        - ``callable_name``: Name of the callable within the module

    Raises
    ------
    SpecValidationError
        If the callable specification string is malformed (contains more than
        one dot) or if the specified module file does not exist. Because import
        is not carried out, the existence of the callable inside the module
        cannot be verified.

    Notes
    -----
    The function supports two specification formats:

    1. **Function name only**: When a value contains no dots:

       - Module: Same basename as the YAML file with .py extension
       - Function: The specified name
       - Example: ``value="my_func"`` with ``sobol_g.yaml`` means
         module ``sobol_g.py``, function ``my_func``

    2. **Fully qualified**: When a value contains exactly one dot:

       - Module: Specified stem with .py extension in the same directory
       - Function: Part after the dot
       - Example: ``value="custom_module.my_func`` means
         module ``custom_module.py``, function ``my_func``

    The ``module_path`` is constructed relative to the parent of ``pkg_root``
    to ensure proper Python import paths within the package structure.
    """

    # --- Validate the string is a valid callable specification
    validate_callable_string(callable_)

    # --- Split the callable string into module and function parts
    # Validation ensures either 'name' or 'module.name' is present
    parts = callable_.split(".")

    if len(parts) == 2:
        # Fully qualified module path
        module_stem, callable_name = parts
        module_file = yaml_file.parent / (module_stem + ".py")
    else:
        # The callable name
        callable_name = parts[0]
        # Assume that the Python module is named the same as the YAML file
        module_file = yaml_file.with_suffix(".py")

    # --- Check that the module file exists
    if not module_file.exists():
        raise SpecValidationError(f"Module file {module_file} does not exist!")

    # --- Construct the module path relative to the package root
    module_path = ".".join(
        module_file.relative_to(pkg_root.parent.resolve())
        .with_suffix("")
        .parts
    )

    return module_path, callable_name
