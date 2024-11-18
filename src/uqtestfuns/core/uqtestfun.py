"""
This module contains the concrete implementation of a generic class to
create a UQ test function in runtime or within a running Python session.
"""

from typing import Callable, Optional

from .uqtestfun_abc import UQTestFunBareABC
from .parameters import FunParams
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
    function_id : str, optional
        The ID of the UQ test function.
    """

    def __init__(
        self,
        evaluate: Callable,
        prob_input: ProbInput,
        parameters: Optional[FunParams] = None,
        function_id: Optional[str] = None,
    ):
        if parameters is None:
            parameters = FunParams()

        self._evaluate = evaluate
        super().__init__(prob_input, parameters, function_id)

    def _eval(self, xx):
        return self._evaluate(xx, **self.parameters.as_dict())

    evaluate = None  # type: ignore
