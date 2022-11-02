"""
Sub-package to model inputs probabilistically.
"""
__all__ = []

from .univariate_input import UnivariateInput
from .multivariate_input import MultivariateInput

from . import univariate_input
from . import multivariate_input

__all__ += ["UnivariateInput", "MultivariateInput"]
__all__ += univariate_input.__all__
__all__ += multivariate_input.__all__
