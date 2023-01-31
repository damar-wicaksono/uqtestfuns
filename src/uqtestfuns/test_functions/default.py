"""
Module that exposes top-level functionalities to create default test functions.

A default function means that the input specification, parameters, and
spatial dimension (when applicable) used to create the function are taken from
the available built-in default values.
"""
from typing import Callable, Any, Optional, Union
from types import ModuleType

from . import (
    ackley,
    borehole,
    damped_oscillator,
    flood,
    ishigami,
    otl_circuit,
    piston,
    sobol_g,
    sulfur,
    wing_weight,
)
from ..core import UQTestFun, MultivariateInput

__all__ = ["get_default_args", "create_from_default", "AVAILABLE_FUNCTIONS"]


# Register all the test functions with implementations here
AVAILABLE_FUNCTIONS = {
    ackley.DEFAULT_NAME.lower(): ackley,
    borehole.DEFAULT_NAME.lower(): borehole,
    damped_oscillator.DEFAULT_NAME.lower(): damped_oscillator,
    flood.DEFAULT_NAME.lower(): flood,
    ishigami.DEFAULT_NAME.lower(): ishigami,
    otl_circuit.DEFAULT_NAME.lower(): otl_circuit,
    piston.DEFAULT_NAME.lower(): piston,
    sobol_g.DEFAULT_NAME.lower(): sobol_g,
    sulfur.DEFAULT_NAME.lower(): sulfur,
    wing_weight.DEFAULT_NAME.lower(): wing_weight,
}


def get_default_args(
    fun_name: str,
    spatial_dimension: Optional[int] = None,
    prob_input: Optional[Union[str, MultivariateInput]] = None,
    parameters: Optional[Any] = None,
) -> dict:
    """Get the arguments to instantiate a UQTestFun from the default selection.

    Parameters
    ----------
    fun_name : str
        Test function name, it must be already registered in the module-level
        constant ``AVAILABLE_FUNCTIONS``.
    spatial_dimension : int, optional
        When applicable, the spatial dimension of the test function.
        Some test functions support variable dimension.
        If the test function does not support variable dimension, passing
        inconsistent dimension returns an error.
    prob_input : Union[str, MultivariateInput]], optional
        The probabilistic input model for the test function.
        When applicable, the input may also be a keyword for selecting
        one of the available input specifications of a test function delivered
        in UQTestFuns.
        Some test functions may be delivered with different
        input specifications based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.
    parameters : Any, optional
        The parameters set of a test function.
        When applicable, the parameters may also be a keyword for selecting
        one of the available parameters set of a test function delivered
        in UQTestFuns.
        Some test functions may have different parameter
        values based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.

    Returns
    -------
    dict
        A dictionary to construct an instance of UQTestFun using the default
        setting for the selected test function.
    """

    # Assertion about spatial dimension
    if spatial_dimension is not None:
        assert spatial_dimension > 0, "Spatial dimension must be >= 0!"

    fun_name = fun_name.lower()

    fun_mod = AVAILABLE_FUNCTIONS[fun_name]

    if isinstance(prob_input, str) or prob_input is None:
        prob_input = _get_default_input(fun_mod, prob_input, spatial_dimension)
    elif isinstance(prob_input, MultivariateInput):
        pass
    else:
        raise TypeError(f"'prob_input' must be {MultivariateInput.__class__}!")

    if isinstance(parameters, str) or parameters is None:
        parameters = _get_default_parameters(
            fun_mod, parameters, spatial_dimension
        )

    default_args = {
        "name": fun_mod.DEFAULT_NAME,
        "evaluate": fun_mod.evaluate,
        "prob_input": prob_input,
        "parameters": parameters,
    }

    return default_args


def create_from_default(
    fun_name: str,
    spatial_dimension: Optional[int] = None,
    prob_input: Optional[Union[str, MultivariateInput]] = None,
    parameters: Optional[Any] = None,
) -> UQTestFun:
    """Create an instance of UQTestFun from the available defaults.

    Parameters
    ----------
    fun_name : str
        Test function name, it must already be registered in the module-level
        constant ``AVAILABLE_FUNCTIONS``.
    spatial_dimension : int
        The spatial dimension of the function, if applicable.
        Some test functions can be defined for an arbitrary spatial dimension.
    prob_input : Union[str, MultivariateInput]], optional
        The probabilistic input model for the test function.
        When applicable, the input may also be a keyword for selecting
        one of the available input specifications of a test function delivered
        in UQTestFuns.
        Some test functions may be delivered with different
        input specifications based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.
    parameters : Any, optional
        The parameters set of a test function.
        When applicable, the parameters may also be a keyword for selecting
        one of the available parameters set of a test function delivered
        in UQTestFuns.
        Some test functions may have different parameter
        values based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.

    Returns
    -------
    UQTestFun
        An instance of UQTestFun created using the default setting for the
        selected test function.
    """
    default_args = get_default_args(
        fun_name,
        spatial_dimension,
        prob_input,
        parameters,
    )

    return UQTestFun(**default_args)


def _get_default_input(
    fun_module: ModuleType,
    selection: Optional[str] = None,
    spatial_dimension: Optional[int] = None,
) -> MultivariateInput:
    """Get the input specification of a test function from the module.

    Parameters
    ----------
    fun_module : ModuleType
        The module in which a test function was implemented.
    selection : str, optional
        The keyword selection of input specification. The selection must
        be implemented in the module; otherwise, an error is thrown.
        With 'None', the default value is used.
    spatial_dimension : str, optional
        The spatial dimension of the input specification. Some test function
        supports variable spatial dimension. In such cases, the dimensionality
        of the input is determined by the user-input dimension.
        With 'None', the default value is used.
        If the function is of fixed-dimension; passing a spatial dimension
        other than the fixed dimension returns an error.

    Returns
    -------
    dict
        The default input specification as a dictionary stored / created
        from the relevant implementation module.
    """
    # Get the default input specification
    if selection is None:
        selection = fun_module.DEFAULT_INPUT_SELECTION

    # Check if the selection is valid
    if selection not in fun_module.AVAILABLE_INPUT_SPECS:
        raise ValueError(
            f"Selected input specification ({selection!r}) is not available!\n"
            f"Either specify 'None' (use the default) or one of "
            f"{list(fun_module.AVAILABLE_INPUT_SPECS.keys())} \n"
            f"for the {fun_module.DEFAULT_NAME!r} test function."
        )

    default_input_specs = fun_module.AVAILABLE_INPUT_SPECS[selection]

    # Get the default dimension
    if _is_variable_dimension(fun_module):
        if spatial_dimension is None:
            spatial_dimension = fun_module.DEFAULT_DIMENSION
    else:
        _verify_spatial_dimension(
            spatial_dimension, default_input_specs, fun_module.DEFAULT_NAME
        )

    # Get the default values to construct a MultivariateInput
    default_name = default_input_specs["name"]
    default_description = default_input_specs["description"]
    default_marginals = default_input_specs["marginals"]
    default_copulas = default_input_specs["copulas"]

    if isinstance(default_marginals, Callable):  # type: ignore
        default_marginals = default_marginals(spatial_dimension)

    default_input = MultivariateInput(
        name=default_name,
        description=default_description,
        marginals=default_marginals,
        copulas=default_copulas,
    )

    return default_input


def _get_default_parameters(
    fun_module: ModuleType,
    selection: Optional[str] = None,
    spatial_dimension: Optional[int] = None,
) -> Any:
    """Get the default parameters used in the evaluation of the function.

    Parameters
    ----------
    fun_module : ModuleType
        The module in which a test function was implemented.
    selection : str, optional
        The keyword selection of parameters set. The selection must
        be implemented in the module; otherwise, an error is thrown.
        With 'None', the default value is used.
    spatial_dimension : str, optional
        The spatial dimension of the input specification. Some test function
        supports variable spatial dimension. In such cases, the parameters
        may follow the number of dimensions.
        With 'None', the default value is used.
        If the function is of fixed-dimension; passing a spatial dimension
        other than the fixed dimension returns an error.

    Returns
    -------
    tuple
        The selected parameters.
    """
    if fun_module.AVAILABLE_PARAMETERS is None:
        if selection is not None:
            raise ValueError(
                f"There is only one parametrization of "
                f"the {fun_module.DEFAULT_NAME!r} test function."
            )

        return None

    if selection is None:
        selection = fun_module.DEFAULT_PARAMETERS_SELECTION

    # Check if the selection is valid
    if selection not in fun_module.AVAILABLE_PARAMETERS:
        raise ValueError(
            f"Selected parameters ({selection!r}) is not available!\n"
            f"Either specify 'None' (use the default) or one of "
            f"{list(fun_module.AVAILABLE_PARAMETERS.keys())} \n"
            f"for the {fun_module.DEFAULT_NAME!r} test function."
        )

    default_parameters = fun_module.AVAILABLE_PARAMETERS[selection]

    # Get the default dimension
    if _is_variable_dimension(fun_module):
        if spatial_dimension is None:
            spatial_dimension = fun_module.DEFAULT_DIMENSION

    if isinstance(default_parameters, Callable):  # type: ignore
        default_parameters = default_parameters(spatial_dimension)

    return default_parameters


def _is_variable_dimension(fun_module: ModuleType) -> bool:
    """Check if the test function is of variable dimension.

    Parameters
    ----------
    fun_module : ModuleType
        The module in which a test function was implemented.
        The information regarding default dimension is stored therein.

    Returns
    -------
    bool
        True if the test function is of variable dimension; False otherwise.
    """
    try:
        _ = fun_module.DEFAULT_DIMENSION
        return True
    except AttributeError:
        return False


def _verify_spatial_dimension(
    spatial_dimension: int,
    default_input_specs: dict,
    fun_name: str,
):
    """Verify the specified spatial dimension given the default.

    Parameters
    ----------
    spatial_dimension : int
        The user-specified spatial dimension.
    default_input : MultivariateInput
        The default input specification.
    fun_name : str
        The name of the test function.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the user-specified dimension is not consistent with the dimension
        stored in the module.
    """
    default_spatial_dimension = len(default_input_specs["marginals"])

    if spatial_dimension is not None:
        assert spatial_dimension == default_spatial_dimension, (
            f"The spatial dimension for the {fun_name!r} test function "
            f"is fixed to {default_spatial_dimension} "
            f"(but {spatial_dimension} is specified instead)."
        )
