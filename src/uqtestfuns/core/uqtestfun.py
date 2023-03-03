"""
This module contains the concrete implementation of a generic class to
create a UQ test function in runtime or within a running Python session.
"""
from typing import Any, Callable, Optional

from .uqtestfun_abc import UQTestFunABC
from .prob_input.probabilistic_input import ProbInput

__all__ = ["UQTestFun"]


class UQTestFun(UQTestFunABC):
    """Generic concrete class of UQ test function."""

    _TAGS = None

    _AVAILABLE_INPUTS = None

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = None

    _DESCRIPTION = None

    def __init__(
        self,
        evaluate: Callable,
        prob_input: Optional[ProbInput] = None,
        parameters: Optional[Any] = None,
        name: Optional[str] = None,
    ):
        self._evaluate = evaluate

        super().__init__(prob_input, parameters, name)

    def evaluate(self, xx):
        if self.parameters is None:
            return self._evaluate(xx)
        else:
            return self._evaluate(xx, self.parameters)
