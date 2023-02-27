"""
This is the package init for UQTestFuns.
"""
from importlib.metadata import version

from .core import UnivDist
from .core import ProbInput
from .core import UQTestFunABC
from .core import UQTestFun

from . import test_functions
from .test_functions import *  # noqa

from .meta import UQMetaFunSpec
from .meta import UQMetaTestFun

from .helpers import list_functions

__version__ = version("uqtestfuns")

__all__ = [
    "UnivDist",
    "ProbInput",
    "UQTestFunABC",
    "UQTestFun",
    "test_functions",
    "UQMetaFunSpec",
    "UQMetaTestFun",
    "list_functions",
]
