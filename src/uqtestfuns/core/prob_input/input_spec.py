"""
Module with definition of data structure to hold information on prob. input.

The probabilistic input specification should be stored in a built-in Python
data type that contains the only information required to construct
a ProbInput instance. The container type should be free of custom methods.
"""
from typing import Any, Callable, List, NamedTuple, Optional, Tuple, Union


__all__ = ["MarginalSpec", "ProbInputSpec", "ProbInputSpecVarDim"]


class MarginalSpec(NamedTuple):
    """A univariate marginal distribution specification.

    Parameters
    ----------
    name : str
        The name of the univariate marginal.
    distribution : str
        The name of the distribution of the univariate marginal.
    parameters : Union[List[Union[int, float]], Tuple[Union[int, float], ...]]
        Parameter values of the distribution.
    description : str
        Short description of the univariate marginal.
    """

    name: str
    distribution: str
    parameters: Union[List[Union[int, float]], Tuple[Union[int, float], ...]]
    description: str


class ProbInputSpec(NamedTuple):
    """All the information required for constructing a ProbInput instance.

    Parameters
    ----------
    name : str
        The name of the probabilistic input model.
    description : str
        A short description of the probabilistic input model.
    marginals : Union[Callable, List[MarginalSpec]]
        A list of univariate marginal specifications or a callable
        to construct the list of marginal specifications.
    copulas : Optional[Any]
        The copula specification of the probabilistic input model.
    """

    name: str
    description: str
    marginals: List[MarginalSpec]
    copulas: Optional[Any]


class ProbInputSpecVarDim(NamedTuple):
    """All the information to construct a ProbInput w/ variable dimension."""

    name: str
    description: str
    marginals_generator: Callable[[int], List[MarginalSpec]]
    copulas: Optional[Any]
