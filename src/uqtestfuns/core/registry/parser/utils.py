"""Utility functions for parsing YAML specification files.

This module provides helper functions for loading, parsing, and resolving
values from YAML specification files used to define UQ test functions. It
includes utilities for:

- Safe loading of YAML files
- Parsing callable specifications (module paths and function names)
- Parsing factory function specifications
"""

import yaml

from pathlib import Path
from string import Template
from typing import Any, Dict, Optional, Tuple

from uqtestfuns.core.registry.specs import CallableSpec

from .expression import resolve_generic
from .validation import SpecValidationError, validate_callable_string


def safe_load(yaml_file: Path) -> dict:
    """Load and parse a YAML file using safe loading.

    This helper function reads a YAML specification file and parses it
    into a Python dictionary using PyYAML's safe_load method, which
    prevents arbitrary code execution and only constructs simple Python
    objects (strings, lists, dicts, numbers, dates, etc.).

    Parameters
    ----------
    yaml_file : Path
        Path to the YAML file to be loaded.

    Returns
    -------
    dict
        Parsed YAML content as a Python dictionary containing the
        specification data.

    Notes
    -----
    - This function uses `yaml.safe_load()` rather than `yaml.load()` to
      ensure security by preventing the execution of arbitrary Python code
      that might be embedded in malicious YAML files.
    """
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    return data


def parse_factory(
    factory_dict: Dict[str, Any],
    spec_file: Path,
    pkg_root: Path,
) -> CallableSpec:
    """Parse a factory function specification from a dictionary.

    This function processes a dictionary containing factory function
    specifications (typically from a YAML file) and converts it into a
    CallableSpec object. It resolves the factory function's module path and
    name, and processes any keyword arguments that should be passed to the
    factory function.

    Parameters
    ----------
    factory_dict : Dict[str, Any]
        Dictionary containing the factory specification. Must include a
        'factory' key with the callable specification string. Any additional
        keys are treated as keyword arguments to be passed to the factory
        function.
    spec_file : Path
        Path to the YAML specification file, used to resolve relative module
        paths for the factory function.
    pkg_root : Path
        Root path of the package, used to construct the absolute module path
        relative to the package structure.

    Returns
    -------
    CallableSpec
        A specification object containing the fully qualified module path,
        function name, and keyword arguments (if any) for the factory function.

    Notes
    -----
    - The 'factory' key is required in the dictionary and specifies the
      callable to be used as the factory function; we assumed this has been
      verified.
    - All other keys in the dictionary are treated as keyword arguments and
      their values are resolved using `resolve_generic()`.
    - If no keyword arguments are present (only 'factory' key exists), the
      kwargs field in the returned CallableSpec will be None.
    - Values in keyword arguments support expression syntax (e.g., '$(pi)')
      for mathematical constants.
    """
    # Parse module path and callable name
    factory_value = factory_dict["factory"]
    module_path, callable_name = parse_callable(
        factory_value,
        spec_file,
        pkg_root,
    )

    # Parse kwargs
    kwargs: Optional[Dict[str, Any]]
    kwargs = {
        k: resolve_generic(v)
        for k, v in factory_dict.items()
        if k != "factory"
    }
    if not kwargs:
        kwargs = None

    return CallableSpec(
        module_path=module_path,
        function_name=callable_name,
        kwargs=kwargs,
    )


def parse_callable(
    callable_string: str,
    spec_file: Path,
    pkg_root: Path,
) -> Tuple[str, str]:
    """Parse a callable spec string into the module path and the function name.

    This helper function parses a callable specification string (typically from
    a YAML file) and resolves it into a fully qualified Python module path and
    a function name. It supports both explicit ``module.function`` notation and
    implicit module resolution based on the YAML file name.

    Parameters
    ----------
    callable_string : str
        The callable specification string. The possible values are:

        - A function name only (e.g., ``my_function``): Uses the specified
          function name from a module with the same name as the YAML file
        - A fully qualified path (e.g., ``my_module.my_function``): Uses the
          specified module file and function name
    spec_file : Path
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
    validate_callable_string(callable_string)

    # --- Split the callable string into module and function parts
    # Validation ensures either 'name' or 'module.name' is present
    parts = callable_string.split(".")

    if len(parts) == 2:
        # Fully qualified module path
        module_stem, callable_name = parts
        module_file = spec_file.parent / (module_stem + ".py")
    else:
        # The callable name
        callable_name = parts[0]
        # Assume that the Python module is named the same as the YAML file
        module_file = spec_file.with_suffix(".py")

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


def substitute_idx(template_str, idx):
    """Substitute the $idx placeholder in a template string.

    Parameters
    ----------
    template_str : str or None
        A string potentially containing ``$idx``.
    idx : int
        The index value to substitute.

    Returns
    -------
    str or None
        The substituted string, or None if the input is None.
    """
    if template_str is None:
        return None

    return Template(template_str).safe_substitute(idx=idx)
