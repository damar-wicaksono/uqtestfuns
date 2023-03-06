"""
This is the package init for UQTestFuns.
"""
import pkg_resources

from .core import UnivDist
from .core import ProbInput
from .core import UQTestFunABC
from .core import UQTestFun

from . import test_functions
from .test_functions import *  # noqa

from .meta import UQMetaFunSpec
from .meta import UQMetaTestFun

from .helpers import list_functions

__version__ = pkg_resources.require("uqtestfuns")[0].version

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
