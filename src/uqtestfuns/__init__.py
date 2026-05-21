"""
This is the package init for UQTestFuns.
"""

import sys

from .core import Marginal
from .core import ProbInput
from .core import (
    UQTestFunBareABC,
    UQTestFunABC,
    UQTestFunFixDimABC,
    UQTestFunVarDimABC,
)
from .core import UQTestFun
from .core import FunParams
from .core import RealVariable
from .core.registry import get_registry

from . import test_functions
from .test_functions import *  # noqa

from .meta import UQMetaFunSpec
from .meta import UQMetaTestFun

from .helpers import list_functions

from . import api
from .api import create, list_parameters

if sys.version_info >= (3, 8):
    from importlib import metadata
else:  # pragma: no cover
    import importlib_metadata as metadata

__version__ = metadata.version("uqtestfuns")

__all__ = [
    "Marginal",
    "ProbInput",
    "FunParams",
    "UQTestFunBareABC",
    "UQTestFunABC",
    "UQTestFunFixDimABC",
    "UQTestFunVarDimABC",
    "UQTestFun",
    "RealVariable",
    "test_functions",
    "UQMetaFunSpec",
    "UQMetaTestFun",
    "list_functions",
    "api",
    "create",
    "list_parameters",
]


# Lazy attribute access: registered test function names are resolved
# to factory callables via the registry on first access.
def __getattr__(name: str):
    registry = get_registry()
    if name in registry:
        return registry.get_factory(name)
    raise AttributeError(f"module 'uqtestfuns' has no attribute {name!r}")


# Include registered test function names in dir() so that
# tab-completion and introspection tools can discover them.
def __dir__():
    registry = get_registry()
    return sorted(list(globals()) + list(registry))
