"""
Utility module used across package.
"""

import os
import inspect

from importlib import import_module
from typing import List, Optional, Tuple, Any
from types import ModuleType

SUPPORTED_TAGS = [
    "sensitivity",
    "optimization",
    "metamodeling",
    "reliability",
    "integration",
]


def get_available_classes(
    package: ModuleType, exclude: Optional[List[str]] = None
) -> List[Tuple[str, Any]]:
    """Get the available classes within a given package.

    Parameters
    ----------
    package : ModuleType
        Fully-qualified package name whose contents (all modules)
        are searched through.
    exclude : Optional[List[str]]
        List of modules within package to exclude (don't include '.py').

    Returns
    -------
    List[Tuple[str, str]]
        List of tuples each element of which is the found class name and
        the fully-qualified class path.
    """

    if exclude is None:
        exclude = []

    # Verify package
    err_msg = f"Invalid package name {package}!"
    try:
        package_file = package.__file__
        if package_file is None:
            raise ValueError(err_msg)
    except AttributeError:
        raise AttributeError(err_msg)

    # Get the full path of a (sub-) package
    package_dir = os.path.dirname(package_file)

    # Get all modules within the package
    all_modules = os.listdir(package_dir)

    classes = []
    for module in all_modules:
        if module.endswith(".py"):
            # Create the full module name
            module_name = f"{package.__name__}.{module.replace('.py', '')}"
            if module_name not in exclude:
                all_members = import_module(module_name)
                all_classes = inspect.getmembers(all_members, inspect.isclass)
                for class_name, class_path in all_classes:
                    if class_path.__module__ == module_name:
                        # This is the class that is defined in the module
                        classes.append((class_name, class_path))

    return classes
