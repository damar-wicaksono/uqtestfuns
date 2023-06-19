"""
Module with definition of data structure to hold information on prob. input.

A probabilistic input specification may be stored in a built-in Python
data type that contains the only information required to construct
a ``UnivDist`` (for one-dimensional marginals) and ``ProbInput``
(for probabilistic input models) instances.
The container type should be free of custom methods and derived from
``NamedTuple`` class to provide typing information.
"""
from typing import Any, Callable, List, NamedTuple, Optional, Tuple, Union


__all__ = ["UnivDistSpec", "ProbInputSpecFixDim", "ProbInputSpecVarDim"]


class UnivDistSpec(NamedTuple):
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

    name: Optional[str]
    distribution: str
    parameters: Union[List[Union[int, float]], Tuple[Union[int, float], ...]]
    description: Optional[str]


class ProbInputSpecFixDim(NamedTuple):
    """All the information to construct a ProbInput w/ a fixed dimension.

    Parameters
    ----------
    name : str
        The name of the probabilistic input model.
    description : str
        A short description of the probabilistic input model.
    marginals : Union[Callable, List[UnivDistSpec]]
        A list of univariate marginal specifications or a callable
        to construct the list of marginal specifications.
    copulas : Optional[Any]
        The copula specification of the probabilistic input model.
    """

    name: Optional[str]
    description: Optional[str]
    marginals: List[UnivDistSpec]
    copulas: Optional[Any]


class ProbInputSpecVarDim(NamedTuple):
    """All the information to construct a ProbInput w/ variable dimension."""

    name: Optional[str]
    description: Optional[str]
    marginals_generator: Callable[[int], List[UnivDistSpec]]
    copulas: Optional[Any]
