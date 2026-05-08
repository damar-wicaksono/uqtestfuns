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

    # Get default input_id
    default_input_id = info.default_input_id

    # Get default parameters_id
    default_parameters_id = info.default_parameters_id

    def factory(
        input_dimension: Optional[int] = None,
        *,
        input_id: str = default_input_id,
        parameters_id: Optional[str] = default_parameters_id,
    ) -> UQTestFun:

        default_input_dim = info.input_dimension
        if default_input_dim is None:
            # Variable-dimension: dimension is required
            if input_dimension is None:
                raise ValueError(
                    f"'{info.name}' is a variable-dimension function; "
                    f"input_dimension must be provided"
                )
            input_dim = input_dimension
        else:
            # Fixed-dimension: ignore or validate user-supplied value
            if input_dimension is not None:
                input_dim = input_dimension
            else:
                input_dim = default_input_dim

            if input_dim != default_input_dim:
                raise ValueError(
                    f"'{info.name}' has fixed input dimension "
                    f"{default_input_dim}, got {input_dim}"
                )

        return _instantiate(spec, info, input_dim, input_id, parameters_id)

    factory.__name__ = info.name
    factory.__qualname__ = info.name
    factory.__doc__ = info.description

    return factory


def _instantiate(
    spec: UQTestFunSpec,
    info: UQTestFunInfo,
    input_dimension: int,
    input_id: str,
    parameters_id: Optional[str],
) -> UQTestFun:
    """Create a UQTestFun instance from specification and metadata.

    This helper function resolves and validates all components needed to
    instantiate a UQTestFun object, including the evaluation callable,
    probabilistic input, and optional parameters.

    Parameters
    ----------
    spec : UQTestFunSpec
        The specification containing callable definitions and configurations.
    info : UQTestFunInfo
        Metadata about the test function including dimension constraints.
    input_dimension : int
        The number of input dimensions for the test function.
    input_id : str
        Identifier for selecting the probabilistic input configuration.
    parameters_id : Optional[str]
        Identifier for selecting parameter configuration, or None if no
        parameters are needed.

    Returns
    -------
    UQTestFun
        A fully configured UQTestFun instance.

    Raises
    ------
    ValueError
        If input_dimension does not match the fixed dimension,
        if input_id is not among the available inputs,
        or if parameters_id is missing or invalid for a parameterized
        function.
    """

    # Resolve probabilistic input
    if input_id not in info.available_input_ids:
        raise ValueError(
            f"Input ID '{input_id}' is not available "
            f"for function '{info.name}'"
        )
    input_spec = spec.inputs[input_id]
    prob_input = resolve_prob_input(input_spec, input_dimension)

    # Resolve parameters
    if spec.parameters is None:
        parameters = None
    else:
        if parameters_id is None:
            raise ValueError(
                f"Parameter ID must be specified for function '{info.name}'"
            )
        if parameters_id not in info.available_parameters_ids:
            raise ValueError(
                f"Parameter ID '{parameters_id}' is not available "
                f"for function '{info.name}'"
            )
        parameters_spec = spec.parameters[parameters_id]
        parameters = resolve_parameters(parameters_spec, input_dimension)

    # Resolve evaluate
    evaluate = resolve_evaluate(spec.evaluate, parameters)

    # Create an instance of UQTestFun
    return UQTestFun(
        evaluate=evaluate,
        prob_input=prob_input,
        parameters=parameters,
        name=info.name,
        description=info.description,
    )
