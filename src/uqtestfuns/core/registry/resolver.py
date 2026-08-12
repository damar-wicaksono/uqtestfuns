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
from typing import Any, Callable, Dict, List, Optional

from .specs import (
    CallableSpec,
    MarginalTemplate,
    UQInputSpec,
    UQParametersSpec,
)
from uqtestfuns.core.prob_input.marginal import Marginal
from uqtestfuns.core.parameters import Parameters
from uqtestfuns.core.registry.parser import SpecValidationError
from uqtestfuns.core.prob_input.probabilistic_input import ProbInput
from uqtestfuns.core.registry.parser.utils import substitute_idx


def resolve_evaluate(
    evaluate_spec: CallableSpec,
    parameters: Optional[Parameters],
) -> Callable:
    """Resolve an evaluate CallableSpec to a callable evaluation function.

    Resolves the callable from the specification and validates that its
    signature matches the provided parameters. The function assumes the
    first argument of the resolved callable is named 'xx' (the input array)
    and verifies that all remaining keyword arguments match the parameter
    keys exactly.

    Parameters
    ----------
    evaluate_spec : CallableSpec
        A specification object containing the module path, function name,
        and optional kwargs for the evaluation function.
    parameters : Parameters, optional
        The parameters object containing keyword arguments that will be
        passed to the evaluation function. If None, no signature validation
        is performed.

    Returns
    -------
    Callable
        The resolved evaluation function, ready to be called with input
        arrays and parameter keyword arguments.

    Raises
    ------
    SpecValidationError
        If the function signature does not match the provided parameters,
        or if the callable cannot be resolved from the specification.
    """
    evaluate = resolve_callable(evaluate_spec)

    # --- Validate the keyword arguments in the 'evaluate' function
    if parameters is not None:
        sig = inspect.signature(evaluate)
        # Assume "xx" is always the first argument of 'evaluate'
        sig_params = set(sig.parameters) - {"xx"}
        # Extra keyword arguments as specified in the parameters
        param_keys = set(parameters.keys())
        if sig_params != param_keys:
            raise SpecValidationError(
                f"{_fullname(evaluate)}: The specified keyword arguments "
                f"{param_keys} do not match function signature {sig_params}"
            )

    return evaluate


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
        raw_marginals = _invoke_factory(func, input_dimension)
        for raw_marginal in raw_marginals:
            marginals.append(
                Marginal(
                    name=raw_marginal["name"],
                    description=raw_marginal["description"],
                    distribution=raw_marginal["distribution"],
                    parameters=raw_marginal["parameters"],
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
            values[keyword] = _invoke_factory(func, input_dimension)
        else:
            values[keyword] = value

    return Parameters(
        name=name,
        keyword_descriptions=kw_descriptions,
        values=values,
        _protected=True,  # This parameter instance is protected
    )


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


# --- Internal helpers


def _fullname(func: Callable[..., Any]) -> str:
    """Return the fully qualified name of a callable.

    Parameters
    ----------
    func : Callable
        The callable whose full name to retrieve.

    Returns
    -------
    str
        The fully qualified name in the form 'module.qualname',
        or repr(func) if either attribute is unavailable.
    """
    module = getattr(func, "__module__", None)
    qualname = getattr(func, "__qualname__", None)

    if module is None or qualname is None:
        return repr(func)

    return f"{module}.{qualname}"


def _needs_input_dimension(func: Callable) -> bool:
    """Check if a callable expects 'input_dimension' as its first parameter.

    Parameters
    ----------
    func : Callable
        The callable to inspect.

    Returns
    -------
    bool
        True if the callable's first parameter is named 'input_dimension',
        False otherwise.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters)

    return len(params) > 0 and params[0] == "input_dimension"


def _invoke_factory(func: Callable, input_dimension: int) -> Any:
    """Invoke a factory callable with optional ``input_dimension``  injection.

    Inspects the factory signature to determine whether it expects
    ``input_dimension`` as its first argument and calls it accordingly.
    Used for factory callables that generate marginals lists or parameter
    values, which may or may not depend on the problem dimensionality.

    Parameters
    ----------
    func : Callable
        The factory callable to invoke. May be a plain function or a
        ``functools.partial`` object with pre-bound kwargs.
    input_dimension : int
        The number of input dimensions. Passed to the factory only if
        its signature expects ``input_dimension`` as its first argument.

    Returns
    -------
    Any
        The value returned by the factory. For marginals factories,
        typically a list of marginal dicts. For parameter factories,
        typically a scalar or array literal.

    Raises
    ------
    SpecValidationError
        If the keyword arguments bound to the factory do not match
        its signature.
    """

    try:
        if _needs_input_dimension(func):
            return func(input_dimension)
        else:
            return func()

    except ValueError as exc:
        # Factory may already be bundled with the kwargs as a partial
        func_ = func.func if isinstance(func, partial) else func
        # Get the signature of the factory function
        sig = inspect.signature(func_)
        # Exclude (optional) 'input_dimension' from the signature parameters
        expected_params = set(sig.parameters) - {"input_dimension"}
        if isinstance(func, partial):
            specified_params = set(func.keywords.keys())
        else:
            specified_params = set()
        # Get the full qualified path of the factory
        fname = _fullname(func_)

        raise SpecValidationError(
            f"Factory '{fname}' has unexpected keyword arguments. "
            f"Expected: {expected_params}, got: {specified_params}"
        ) from exc
