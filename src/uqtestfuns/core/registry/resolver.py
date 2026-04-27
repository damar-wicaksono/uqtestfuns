import importlib

from functools import partial
from typing import Callable

from .specs import CallableSpec
from uqtestfuns.core.registry.parser import SpecValidationError


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
