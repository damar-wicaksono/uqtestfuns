"""
This is the package init for uqtestfuns.

"""
from . import core
from . import test_functions

from .core import UQTestFun, UnivariateInput, MultivariateInput
from .test_functions.default import create_from_default, get_default_args
