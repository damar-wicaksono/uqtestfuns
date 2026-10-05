"""Factory functions for creating UQ test function instances.

This module provides utilities for generating callable factories that
instantiate UQTestFun objects from their specifications and metadata.
The factory pattern allows dynamic creation of test functions
with configurable dimensions, input configurations,
and parameters while respecting constraints defined in the function metadata.
"""

from typing import Callable, Optional

from uqtestfuns.core.uqtestfun import UQTestFun
from uqtestfuns.core.registry.entries import UQTestFunInfo, UQTestFunSpec
from uqtestfuns.core.registry.resolver import (
    resolve_evaluate,
    resolve_prob_input,
    resolve_parameters,
)
from uqtestfuns.core.prob_input.probabilistic_input import ProbInput
from uqtestfuns.core.parameters import Parameters


def make_factory(spec: UQTestFunSpec, info: UQTestFunInfo) -> Callable:
    """Create a factory function for instantiating UQ test functions.

    This function generates a callable factory that can be used to create
    UQTestFun instances with configurable input dimensions, input IDs, and
    parameter IDs. The factory respects dimension constraints specified in
    the function metadata and provides appropriate default values.

    Parameters
    ----------
    spec : UQTestFunSpec
        The specification containing callable definitions,
        input configurations, and parameter settings for the test function.
    info : UQTestFunInfo
        Metadata about the test function including name, description, default
        IDs, and dimension constraints.

    Returns
    -------
    Callable
        A factory function that creates UQTestFun instances. The factory
        signature depends on whether the input dimension is fixed or variable.
    """

    def factory(
        input_dimension: Optional[int] = None,
        *,
        input_id: Optional[str] = None,
        parameters_id: Optional[str] = None,
        prob_input: Optional[ProbInput] = None,
        parameters: Optional[Parameters] = None,
    ) -> UQTestFun:

        # --- Select or validate input dimension
        input_dim = _select_or_validate_input_dimension(
            info,
            input_dimension,
            prob_input,
        )

        # --- Select or validate probabilistic input model
        prob_input = _select_or_validate_prob_input(
            spec,
            input_dim,
            input_id,
            prob_input,
        )

        # --- Select or validate parameters
        parameters = _select_or_validate_parameters(
            spec,
            input_dim,
            parameters_id,
            parameters,
        )

        # --- Resolve evaluate
        evaluate = resolve_evaluate(spec.evaluate, parameters)

        return UQTestFun(
            evaluate=evaluate,
            prob_input=prob_input,
            parameters=parameters,
            name=info.name,
            description=info.description,
            output_dimension=info.output_dimension,
        )

    factory.__name__ = info.name
    factory.__qualname__ = info.name
    factory.__doc__ = info.description

    return factory


def _select_or_validate_input_dimension(
    info: UQTestFunInfo,
    input_dimension: int | None,
    prob_input: ProbInput | None,
) -> int:
    """Select or validate the input dimension for a test function.

    The dimension may be specified by up to three sources: the test function's
    default (``info.input_dimension``), an explicitly requested
    ``input_dimension``, and the dimension of a pre-configured ``prob_input``.
    All sources that are present must agree.

    For fixed-dimension functions (``info.input_dimension`` is not ``None``),
    the default is the source of truth; any provided ``input_dimension`` or
    ``prob_input`` dimension must match it. For variable-dimension functions
    (``info.input_dimension`` is ``None``), the dimension must come from
    ``input_dimension`` and/or ``prob_input``, which must agree if both given.

    Parameters
    ----------
    info : UQTestFunInfo
        Test function metadata, including the default dimension which is
        ``None`` for variable-dimension functions.
    input_dimension : int, optional
        The requested input dimension, or ``None`` if not specified.
    prob_input : ProbInput, optional
        A pre-configured probabilistic input instance, or ``None`` if not
        given. Its dimension is treated as another source.

    Returns
    -------
    int
        The validated input dimension.

    Raises
    ------
    ValueError
        For a variable-dimension function, if neither ``input_dimension`` nor
        ``prob_input`` is provided, or if both are provided but disagree.
        For a fixed-dimension function, if ``input_dimension`` or the
        ``prob_input`` dimension is provided but does not match the default.
    """
    default = info.input_dimension
    given = input_dimension
    from_obj = prob_input.dimension if prob_input is not None else None

    if given is not None and given < 1:
        raise ValueError(
            f"Input dimension must be positive, got {input_dimension}"
        )

    if default is None:
        # Variable-dimension: no anchor, candidates must agree and exist.
        if given is not None and from_obj is not None and given != from_obj:
            raise ValueError(
                f"'{info.name}' is variable-dimension, but 'input_dimension' "
                f"({given}) and 'prob_input' dimension ({from_obj}) disagree"
            )
        resolved = given if given is not None else from_obj
        if resolved is None:
            raise ValueError(
                f"'{info.name}' is variable-dimension; "
                f"'input_dimension' or 'prob_input' must be provided"
            )
        return resolved

    # Fixed-dimension: 'default' is the anchor; anything present must match it.
    if given is not None and given != default:
        raise ValueError(
            f"'{info.name}' has fixed input dimension {default}, "
            f"but 'input_dimension' is {given}"
        )
    if from_obj is not None and from_obj != default:
        raise ValueError(
            f"'{info.name}' has fixed input dimension {default}, "
            f"but 'prob_input' dimension is {from_obj}"
        )
    return default


def _select_or_validate_prob_input(
    spec: UQTestFunSpec,
    input_dimension: int,
    input_id: str | None,
    prob_input: ProbInput | None,
) -> ProbInput:
    """Select or validate the probabilistic input for a test function.

    This helper either uses a provided ``ProbInput`` instance or creates one
    from the specification based on the ``input_id``. When creating from the
    specification, it falls back to ``spec.inputs.default_id`` if no
    ``input_id`` is given, and validates that the resolved probabilistic
    input matches the requested ``input_dimension``.

    Parameters
    ----------
    spec : UQTestFunSpec
        The specification containing the available input configurations and
        their default ID.
    input_dimension : int
        The expected input dimension, used to resolve and validate the
        probabilistic input.
    input_id : str, optional
        Identifier for selecting the probabilistic input configuration.
        If ``None``, uses ``spec.inputs.default_id``.
    prob_input : ProbInput, optional
        A pre-configured probabilistic input instance. Mutually exclusive
        with ``input_id``.

    Returns
    -------
    ProbInput
        The resolved and validated probabilistic input.

    Raises
    ------
    ValueError
        If both ``input_id`` and ``prob_input`` are specified, or if the
        resolved ``input_id`` is not available for the function.
    """

    # 'input_id' and 'prob_input' are mutually exclusive
    if input_id is not None and prob_input is not None:
        raise ValueError(
            "Specify either 'input_id' or 'prob_input', not both."
        )

    # 'prob_input' is not provided and must be created
    if prob_input is None:
        default_id = spec.inputs.default_id
        resolved_id = input_id if input_id is not None else default_id
        if resolved_id not in spec.inputs.by_id.keys():
            raise ValueError(
                f"Input ID '{resolved_id}' is not available "
                f"for function '{spec.name}'"
            )
        input_spec = spec.inputs.by_id[resolved_id]
        prob_input = resolve_prob_input(input_spec, input_dimension)

    return prob_input


def _select_or_validate_parameters(
    spec: UQTestFunSpec,
    input_dimension: int,
    parameters_id: str | None,
    parameters_: Parameters | None,
) -> Parameters | None:
    """Select or validate parameters for a test function.

    This helper either uses a provided ``Parameters`` instance or creates one
    from the specification based on the ``parameters_id``. It handles
    functions that take no parameters (``spec.parameters is None``) and, when
    resolving from the specification, falls back to
    ``spec.parameters.default_id`` if no ``parameters_id`` is given.

    Parameters
    ----------
    spec : UQTestFunSpec
        The specification containing the parameter configurations and their
        default ID. ``spec.parameters`` is ``None`` for non-parameterized
        functions.
    input_dimension : int
        The input dimension used for parameter resolution.
    parameters_id : str, optional
        Identifier for selecting the parameter configuration.
        If ``None``, uses ``spec.parameters.default_id``.
    parameters_ : Parameters, optional
        A pre-configured parameters instance. Mutually exclusive with
        ``parameters_id``.

    Returns
    -------
    Parameters or None
        The resolved parameters, or ``None`` if the function takes no
        parameters.

    Raises
    ------
    ValueError
        If both ``parameters_id`` and ``parameters_`` are specified, if
        either is provided for a non-parameterized function, or if the
        resolved ``parameters_id`` is not available for the function.
    """
    # --- Basic checks
    # 'parameters_id' and 'parameters' are mutually exclusive
    if parameters_id is not None and parameters_ is not None:
        raise ValueError(
            "Specify either 'parameters_id' or 'parameters', not both."
        )

    # --- The function is not parameterized
    if spec.parameters is None:
        # 'parameters_id' and 'parameters_' must not be provided simultaneously
        if parameters_id is not None or parameters_ is not None:
            raise ValueError(f"'{spec.name}' takes no parameters")
        return None

    # --- The function is parameterized
    if parameters_ is not None:
        # 'parameters' is provided, return as-is
        return parameters_
    # 'parameters' is not provided, resolve from ID
    default_id = spec.parameters.default_id
    rid = parameters_id if parameters_id is not None else default_id
    if rid not in spec.parameters.by_id.keys():
        raise ValueError(
            f"Parameters ID '{rid}' is not available for '{spec.name}'"
        )

    return resolve_parameters(spec.parameters.by_id[rid], input_dimension)
