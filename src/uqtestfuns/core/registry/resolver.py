"""Resolution utilities for UQ test function specifications.

This module provides functions to resolve parsed specifications into
concrete runtime objects. It handles dynamic imports of callables,
construction of probabilistic input objects from various marginal
representations, and parameter object creation with support for
factory functions.
"""

import importlib
import inspect

from functools import partial
from typing import Any, Callable, Dict, List

from .specs import (
    CallableSpec,
    MarginalTemplate,
    UQInputSpec,
    UQParametersSpec,
)
from uqtestfuns.core.prob_input.marginal import Marginal
from uqtestfuns.core.parameters import Parameters
from uqtestfuns.core.registry.parser import SpecValidationError
from uqtestfuns.core.prob_input.probabilistic_input_new import ProbInput
from uqtestfuns.core.registry.parser.utils import substitute_idx


def resolve_callable(callable_spec: CallableSpec) -> Callable:
    """Resolve a CallableSpec to a callable object.

    Dynamically imports the module specified in the CallableSpec, retrieves
    the named function, and optionally wraps it with ``functools.partial``
    if kwargs are provided.

    Parameters
    ----------
    callable_spec : CallableSpec
        A specification object containing ``module_path``,
        ``function_name``, and optional ``kwargs``.

    Returns
    -------
    Callable
        The resolved callable. If kwargs are provided in the spec,
        a ``functools.partial`` with those kwargs bound; otherwise,
        the original function object.

    Raises
    ------
    SpecValidationError
        If the module cannot be imported, the named attribute does not
        exist in the module, or the attribute is not callable.
    """
    # Fetch the relevant fields
    module_path = callable_spec.module_path
    function_name = callable_spec.function_name
    kwargs = callable_spec.kwargs

    # Import the module
    try:
        mod = importlib.import_module(module_path)
    except Exception as exc:
        # Any exceptions raised are channeled to a single exception
        raise SpecValidationError(
            f"Cannot import module '{module_path}': {exc}"
        ) from exc

    # Get the function from the module
    func = getattr(mod, function_name, None)
    if func is None:
        raise SpecValidationError(
            f"Module '{module_path}' has no attribute '{function_name}'"
        )
    if not callable(func):
        raise SpecValidationError(
            f"Attribute '{function_name}' in module '{module_path}' "
            "is not callable"
        )

    # Resolve the kwargs
    if kwargs:
        func = partial(func, **kwargs)

    return func


def resolve_prob_input(
    prob_input_spec: UQInputSpec,
    input_dimension: int,
) -> ProbInput:
    """Resolve a UQInputSpec to a ProbInput object.

    Constructs a list of Marginal objects from the marginals field
    of the spec, handling three shapes: an explicit list, a template,
    or a factory callable. The resulting marginals and copulas are
    assembled into a ProbInput.

    Parameters
    ----------
    prob_input_spec : UQInputSpec
        A parsed input specification containing ``name``, ``marginals``,
        and ``copulas``.
    input_dimension : int
        The number of input dimensions for the function.

    Returns
    -------
    ProbInput
        The constructed probabilistic input object.

    Raises
    ------
    SpecValidationError
        If the length of the marginals list does not match ``input_dimension``,
        or if the factory callable returns invalid marginal definitions.
    TypeError
        If the marginals field has an unexpected type. This indicates
        a programming error, not a spec issue.
    """
    # Fetch the relevant fields
    name = prob_input_spec.name
    marginals_spec = prob_input_spec.marginals
    copulas_spec = prob_input_spec.copulas

    # Resolve marginals
    marginals: List[Marginal] = []

    if isinstance(marginals_spec, list):
        if len(marginals_spec) != input_dimension:
            raise SpecValidationError(
                f"Input dimension {input_dimension} does not match "
                f"the number of marginals ({len(marginals_spec)})"
            )
        for marginal in marginals_spec:
            marginals.append(
                Marginal(
                    name=marginal.name,
                    description=marginal.description,
                    distribution=marginal.distribution,
                    parameters=marginal.parameters,
                )
            )

    elif isinstance(marginals_spec, MarginalTemplate):
        for i in range(input_dimension):
            marginals.append(
                Marginal(
                    name=substitute_idx(marginals_spec.name, i + 1),
                    description=substitute_idx(
                        marginals_spec.description,
                        i + 1,
                    ),
                    distribution=marginals_spec.distribution,
                    parameters=marginals_spec.parameters,
                )
            )

    elif isinstance(marginals_spec, CallableSpec):
        func = resolve_callable(marginals_spec)
        if _needs_input_dimension(func):
            raw_marginals = func(input_dimension)
        else:
            raw_marginals = func()
        for marginal in raw_marginals:
            marginals.append(
                Marginal(
                    name=marginal["name"],
                    description=marginal["description"],
                    distribution=marginal["distribution"],
                    parameters=marginal["parameters"],
                )
            )

    else:
        raise TypeError(f"Unexpected marginals type: {type(marginals_spec)}")

    return ProbInput(marginals, copulas_spec, name=name)


def resolve_parameters(
    parameters_spec: UQParametersSpec,
    input_dimension: int,
) -> Parameters:
    """Resolve a UQParametersSpec to a Parameters object.

    Iterates over the parameter values in the spec, resolving any
    factory callables to their computed values while passing literal
    values through unchanged.

    Parameters
    ----------
    parameters_spec : UQParametersSpec
        A parsed parameter specification containing ``name``,
        ``keyword_descriptions``, and ``values``.
    input_dimension : int
        The number of input dimensions for the function.

    Returns
    -------
    Parameters
        The constructed parameters object.
    """
    # Fetch the relevant metadata
    name = parameters_spec.name
    kw_descriptions = parameters_spec.keyword_descriptions

    # Fetch values, resolve any callables
    values: Dict[str, Any] = {}
    for keyword, value in parameters_spec.values.items():
        if isinstance(value, CallableSpec):
            func = resolve_callable(value)
            if _needs_input_dimension(func):
                values[keyword] = func(input_dimension)
            else:
                values[keyword] = func()
        else:
            values[keyword] = value

    return Parameters(
        name=name,
        descriptions=kw_descriptions,
        values=values,
    )


def _needs_input_dimension(func: Callable) -> bool:
    """Check if the first parameter of func is 'input_dimension'."""
    sig = inspect.signature(func)
    params = list(sig.parameters)

    return len(params) > 0 and params[0] == "input_dimension"
