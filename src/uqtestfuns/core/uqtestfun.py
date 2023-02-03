"""
uqtestfun.py

This module contains the concrete implementation of a generic class to
create a UQ test function.
"""
from typing import Any, Callable, Optional

from .uqtestfun_abc import UQTestFunABC
from .prob_input.multivariate_input import MultivariateInput

__all__ = ["UQTestFun"]


class UQTestFun(UQTestFunABC):
    """Generic concrete class of UQ test function."""

    tags = None

    available_inputs = None

    available_parameters = None

    default_dimension = None

    def __init__(
        self,
        evaluate: Callable,
        prob_input: Optional[MultivariateInput] = None,
        parameters: Any = None,
        name: str = None,
    ):
        self._evaluate = evaluate

        super().__init__(prob_input, parameters, name)

    def evaluate(self, xx):
        return self._evaluate(xx, self.parameters)
