"""Registry system for UQ test function metadata.

This module provides the Registry class which manages a collection of UQ
(Uncertainty Quantification) test function specifications. The registry loads
and stores metadata about test functions from YAML specification files,
providing a centralized catalog for function discovery, introspection, and
instantiation.

The Registry class acts as a container that:

- Scans directories for YAML specification files
- Parses and validates test function metadata
- Provides dictionary-like access to function information
- Prevents duplicate function registrations
"""

import difflib

from pathlib import Path
from typing import Dict, Callable, Optional

from uqtestfuns.core.registry.entries import UQTestFunInfo
from uqtestfuns.core.registry.factory import make_factory
from uqtestfuns.core.registry.parser import SpecValidationError
from uqtestfuns.core.registry.parser.spec_file import parse_info, parse_spec

DEFAULT_ROOT = Path(__file__).parent.parent.parent / "test_functions"

PKG_ROOT = Path(__file__)
while PKG_ROOT.name != "uqtestfuns":
    PKG_ROOT = PKG_ROOT.parent


class Registry:
    """A registry for UQ test function metadata.

    The Registry class manages a collection of UQ test function specifications
    loaded from YAML files. It provides dictionary-like access to function
    metadata and supports scanning directories for test function
    specifications.

    Attributes
    ----------
    _infos : Dict[str, UQTestFunInfo]
        Internal dictionary mapping function names to their metadata.
    """

    def __init__(self, pkg_root: Path = PKG_ROOT):
        """Initialize an empty Registry."""
        self._infos: Dict[str, UQTestFunInfo] = {}
        self._pkg_root = pkg_root
        self._factories: Dict[str, Callable] = {}

    def scan(self, root: Path):
        """Scan a directory for test function specification files.

        Loads all YAML files in the given directory (excluding files ending
        with '_inputs.yaml') and adds their parsed metadata to the registry.

        Parameters
        ----------
        root : Path
            The directory path to scan for YAML specification files.
        pkg_root : Path
            The root directory of the package.
        Raises
        ------
        SpecValidationError
            If a duplicate function name is found or if YAML parsing fails.
        """
        for yaml_file in root.rglob("*.yaml"):
            if is_inputs_yaml(yaml_file.name):
                continue
            info = parse_info(yaml_file)
            if info.name in self._infos:
                raise SpecValidationError(f"Duplicate entry for {info.name}")
            self._infos[info.name] = info

    @property
    def entries(self) -> Dict[str, UQTestFunInfo]:
        """Return a dictionary of all registered test functions.

        Returns
        -------
        Dict[str, UQTestFunInfo]
            The dictionary of registered test functions metadata.
        """
        return self._infos

    def items(self):
        """Return an iterator over (name, info) pairs.

        Returns
        -------
        dict_items
            An iterator over tuples of (function_name, UQTestFunInfo).
        """
        return self._infos.items()

    def keys(self):
        """Return an iterator over registered function names.

        Returns
        -------
        dict_keys
            An iterator over the names of registered test functions.
        """
        return self._infos.keys()

    def values(self):
        """Return an iterator over UQTestFunInfo objects.

        Returns
        -------
        dict_values
            An iterator over the metadata objects of registered test functions.
        """
        return self._infos.values()

    def __contains__(self, key: str) -> bool:
        """Check if a function is registered.

        Parameters
        ----------
        key : str
            The name of the test function.

        Returns
        -------
        bool
            True if the function is registered, False otherwise.
        """
        return key in self._infos

    def __iter__(self):
        """Return an iterator over registered test function names.

        Returns
        -------
        dict_keys
            An iterator over the names of registered test functions.
        """
        return iter(self._infos)

    def __len__(self):
        """Return the number of registered test functions.

        Returns
        -------
        int
            The count of test functions in the registry.
        """
        return len(self._infos)

    def __getitem__(self, key):
        """Retrieve metadata for a test function by name.

        Parameters
        ----------
        key : str
            The name of the test function.

        Returns
        -------
        UQTestFunInfo
            The metadata object for the requested test function.

        Raises
        ------
        KeyError
            If the function name is not found in the registry.
        """
        if key not in self._infos:
            msg = f"Test function {key!r} not available."
            matches = _suggest_name(key, self._infos.keys())
            if matches is not None:
                msg += f" Did you mean {matches!r}?"
            raise KeyError(msg)

        return self._infos[key]

    def get_factory(self, name: str):
        """Retrieve or create a factory function for a test function.

        Returns a factory callable that can be used to instantiate
        a UQTestFun object with the specified name. The factory is
        created on first access and cached for later calls.

        Parameters
        ----------
        name : str
            The name of the test function.

        Returns
        -------
        Callable
            A factory function that creates UQTestFun instances.

        Raises
        ------
        KeyError
            If the function name is not found in the registry.
        """
        if name not in self._factories:
            info = self[name]
            spec = parse_spec(info.spec_path, self._pkg_root)
            factory = make_factory(spec, info)
            self._factories[name] = factory

        return self._factories[name]


def is_inputs_yaml(filename: str) -> bool:
    """Check if a filename matches input specification file patterns.

    Input specification files follow naming conventions and should be
    excluded from the main test function registry scan. This function
    identifies files that match these patterns.

    Parameters
    ----------
    filename : str
        The filename to check (not the full path, just the name).

    Returns
    -------
    bool
        True if the filename matches any input specification pattern:
        - Ends with '_inputs.yaml'
        - Starts with 'inputs_' and ends with '.yaml'
        - Equals 'inputs.yaml'
    """
    return (
        filename.endswith("_inputs.yaml")
        or (filename.startswith("inputs_") and filename.endswith(".yaml"))
        or filename == "inputs.yaml"
    )


def _suggest_name(name: str, candidates) -> Optional[str]:
    matches = difflib.get_close_matches(name, candidates, n=1, cutoff=0.6)

    return matches[0] if matches else None
