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


from . import test_functions
from .test_functions import *  # noqa

from .meta import UQMetaFunSpec
from .meta import UQMetaTestFun

from .helpers import list_functions

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
    "test_functions",
    "UQMetaFunSpec",
    "UQMetaTestFun",
    "list_functions",
]
