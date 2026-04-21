"""Specifications for callable objects in the registry.

This module contains dataclass specifications used for registering and
managing callable objects in the UQTestFuns registry system.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass(frozen=True)
class CallableSpec:
    """Specification for a callable object with its module path and parameters.

    This immutable dataclass represents a callable object by storing its
    module path, function name, and optional keyword arguments. It is used
    in the registry system to define and instantiate callable objects
    dynamically.

    Parameters
    ----------
    module_path : str
        The full module path where the callable is located (e.g.,
        'uqtestfuns.test_functions.ackley').
    function_name : str
        The name of the callable/function to be retrieved from the module.
    kwargs : Dict[str, Any], optional
        Optional keyword arguments to be passed to the callable when
        instantiated. Default is None.
    """

    module_path: str
    function_name: str
    kwargs: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class MarginalSpec:
    """Specification for a marginal distribution.

    This immutable dataclass represents a marginal distribution by storing
    its distribution type, parameters, and optional metadata. It is used in
    the registry system to define probabilistic input specifications for
    UQ test functions.

    Parameters
    ----------
    distribution : str
        The name/type of the probability distribution (e.g., 'normal',
        'uniform', 'beta').
    parameters : List[Union[float, int]]
        List of distribution parameters. The number and meaning of parameters
        depend on the distribution type (e.g., [mean, std] for normal,
        [lower, upper] for uniform).
    name : str, optional
        An optional name for the marginal distribution. Default is None.
    description : str, optional
        An optional description of the marginal distribution. Default is None.
    """

    distribution: str
    parameters: List[Union[float, int]]
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass(frozen=True)
class MarginalList:
    """Specification for a list of marginal distributions.

    This immutable dataclass represents a collection of marginal distributions
    that together define the probabilistic input space for a UQ test function.
    It is used in the registry system to specify a (multidimensional)
    probabilistic input model where each dimension has its own marginal
    distribution.

    Parameters
    ----------
    sequence : Sequence[MarginalSpec]
        An ordered list of marginal distribution specifications. Each element
        represents the marginal distribution for one input dimension. The
        length of the sequence determines the dimensionality of the input
        space.
    """

    sequence: List[MarginalSpec]


@dataclass(frozen=True)
class MarginalTemplate:
    """Specification for a marginal distribution template.

    This immutable dataclass represents a template for creating multiple
    marginal distributions with the same distribution type and parameters
    but with parameterized names and descriptions. It is used in the registry
    system to define reusable marginal distribution patterns that can be
    instantiated with different naming conventions.

    Parameters
    ----------
    distribution : str
        The name/type of the probability distribution (e.g., 'normal',
        'uniform', 'beta').
    parameters : List[Union[float, int]]
        List of distribution parameters. The number and meaning of parameters
        depend on the distribution type (e.g., [mean, std] for normal,
        [lower, upper] for uniform).
    name_template : str, optional
        An optional template string for the marginal distribution name that
        can contain placeholders for parameterization. Default is None.
    description_template : str, optional
        An optional template string for the marginal distribution description
        that can contain placeholders for parameterization. Default is None.
    """

    distribution: str
    parameters: List[Union[float, int]]
    name_template: Optional[str] = None
    description_template: Optional[str] = None


@dataclass(frozen=True)
class UQInputSpec:
    """Specification for UQ test function input.

    This immutable dataclass represents the complete probabilistic input
    specification for a UQ test function. It combines marginal distributions
    (which define the behavior of individual input dimensions) with optional
    copulas (which define dependencies between input dimensions). It is used
    in the registry system to specify the full probabilistic input model
    for uncertainty quantification test functions.

    Parameters
    ----------
    marginals : Union[MarginalSpec, MarginalList, MarginalTemplate]
        The marginal distribution specification(s) for the input dimensions.
        Can be a single MarginalSpec (for one-dimensional inputs), a
        MarginalList (for multi-dimensional inputs with different marginals
        for each dimension), or a MarginalTemplate (for creating multiple
        similar marginals from a template).
    copulas : Any, optional
        Optional copula specification that defines the dependence structure
        between input dimensions. If None, independence between dimensions
        is assumed. Default is None. This feature is not yet supported.
    """

    marginals: Union[MarginalList, MarginalTemplate, CallableSpec]
    copulas: Optional[Any] = None


@dataclass(frozen=True)
class UQParametersSpec:
    """Specification for UQ test function parameters.

    This immutable dataclass represents the parameters of a UQ test function,
    including their values and optional descriptions. It is used in the
    registry system to specify configurable parameters that affect the
    behavior of uncertainty quantification test functions.

    Parameters
    ----------
    descriptions : Dict[str, str], optional
        Optional dictionary mapping parameter names to their human-readable
        descriptions. This provides documentation for what each parameter
        represents and how it affects the test function. Default is None.
    values : Dict[str, Any]
        Dictionary mapping parameter names to their values. The keys are
        parameter names (strings) and the values can be of any type
        appropriate for the parameter (e.g., float, int, str, list).
    """

    descriptions: Optional[Dict[str, str]]
    values: Dict[str, Any]
