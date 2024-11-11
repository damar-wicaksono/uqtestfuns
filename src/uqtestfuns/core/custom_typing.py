"""
Core module that contains custom types used in UQTestFuns.

Custom types are used to assist type checker during the code development.
"""

from typing import Callable, List, Union, Optional, Any, Dict, Sequence
from typing_extensions import TypedDict

from uqtestfuns.core.prob_input.marginal import Marginal

__all__ = [
    "MarginalSpec",
    "MarginalSpecs",
    "ProbInputSpecs",
    "ProbInputArgs",
    "FunParamSpecs",
    "FunParamsArgs",
    "DeclaredParameters",
]


class MarginalSpec(TypedDict):
    name: str
    distribution: str
    parameters: List[Union[float, int]]
    description: Optional[str]


MarginalSpecs = List[MarginalSpec]


class ProbInputSpec(TypedDict):
    function_id: str
    description: str
    marginals: Union[List[MarginalSpec], Callable]
    copulas: Optional[Any]


ProbInputSpecs = Dict[str, ProbInputSpec]


class ProbInputArgs(TypedDict):
    function_id: str
    input_id: str
    description: str
    marginals: Sequence[Marginal]
    copulas: Optional[Any]


class DeclaredParameter(TypedDict):
    keyword: str
    value: Any
    type: Optional[type]
    description: Optional[str]


DeclaredParameters = List[DeclaredParameter]


class FunParamsSpec(TypedDict):
    function_id: str
    description: str
    declared_parameters: DeclaredParameters


FunParamSpecs = Dict[str, FunParamsSpec]


class FunParamsArgs(TypedDict):
    function_id: str
    parameter_id: str
    description: str
    declared_parameters: DeclaredParameters
