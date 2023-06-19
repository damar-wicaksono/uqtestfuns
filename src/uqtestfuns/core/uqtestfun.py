"""
This module contains the concrete implementation of a generic class to
create a UQ test function in runtime or within a running Python session.
"""
from typing import Any, Callable, Optional

from .uqtestfun_abc import UQTestFunBareABC
from .prob_input.probabilistic_input import ProbInput

__all__ = ["UQTestFun"]


class UQTestFun(UQTestFunBareABC):
    """Generic concrete class of UQ test function.

    Parameters
    ----------
    evaluate : Callable
        The evaluation function of the UQ test function implemented as a
        Python callable.
    prob_input : ProbInput
        The probabilistic input model of the UQ test function.
    parameters : Any, optional
        The parameters set of the UQ test function.
        If not specified, `None` is used.
    name : str, optional
        The name of the UQ test function.
    """

    def __init__(
        self,
        evaluate: Callable,
        prob_input: ProbInput,
        parameters: Optional[Any] = None,
        name: Optional[str] = None,
    ):
        self._evaluate = evaluate
        super().__init__(prob_input, parameters, name)

    def evaluate(self, xx):
        if self.parameters is not None:
            return self._evaluate(xx, self.parameters)

        return self._evaluate(xx)
