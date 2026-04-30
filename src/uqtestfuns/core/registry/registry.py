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

from pathlib import Path
from typing import Dict

from uqtestfuns.core.registry.entries import UQTestFunInfo
from uqtestfuns.core.registry.parser import SpecValidationError
from uqtestfuns.core.registry.parser.spec_file import parse_info

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
    _entries : Dict[str, UQTestFunInfo]
        Internal dictionary mapping function names to their metadata.
    """

    def __init__(self, pkg_root: Path = PKG_ROOT):
        """Initialize an empty Registry."""
        self._entries: Dict[str, UQTestFunInfo] = {}
        self._pkg_root = pkg_root

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
            if info.name in self._entries:
                raise SpecValidationError(f"Duplicate entry for {info.name}")
            self._entries[info.name] = info

    @property
    def entries(self) -> Dict[str, UQTestFunInfo]:
        """Return a dictionary of all registered test functions.

        Returns
        -------
        Dict[str, UQTestFunInfo]
            The dictionary of registered test functions metadata.
        """
        return self._entries

    def items(self):
        """Return an iterator over (name, info) pairs.

        Returns
        -------
        dict_items
            An iterator over tuples of (function_name, UQTestFunInfo).
        """
        return self._entries.items()

    def keys(self):
        """Return an iterator over registered function names.

        Returns
        -------
        dict_keys
            An iterator over the names of registered test functions.
        """
        return self._entries.keys()

    def values(self):
        """Return an iterator over UQTestFunInfo objects.

        Returns
        -------
        dict_values
            An iterator over the metadata objects of registered test functions.
        """
        return self._entries.values()

    def __len__(self):
        """Return the number of registered test functions.

        Returns
        -------
        int
            The count of test functions in the registry.
        """
        return len(self._entries)

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
        return self._entries[key]


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
