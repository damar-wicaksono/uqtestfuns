"""
Module that exposes top-level functionalities to create default test functions.

A default function means that the input specification, parameters, and
spatial dimension (when applicable) used to create the function are taken from
the available built-in default values.
"""
from typing import Callable
from types import ModuleType

from . import wing_weight, ishigami, borehole, ackley
from ..core import UQTestFun

__all__ = ["get_default_args", "create_from_default", "AVAILABLE_FUNCTIONS"]


# Register all the test functions with implementations here
AVAILABLE_FUNCTIONS = {
    borehole.DEFAULT_NAME.lower(): borehole,
    ishigami.DEFAULT_NAME.lower(): ishigami,
    wing_weight.DEFAULT_NAME.lower(): wing_weight,
    ackley.DEFAULT_NAME.lower(): ackley,
}


def get_default_args(
    fun_name: str,
    spatial_dimension: int = None,
    input_selection: str = None,
    param_selection: str = None,
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
    input_selection : str, optional
        When applicable, the keyword for selecting the input specification of
        a test function. Some test functions may be delivered with different
        input specifications based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.
    param_selection : str, optional
        When applicable, the keyword for selecting the parameters set of
        a test function. Some test functions may have different parameter values
        based on the available literature.
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

    default_args = {
        "name": fun_mod.DEFAULT_NAME,
        "evaluate": fun_mod.evaluate,
        "input": _get_default_input(
            fun_mod,
            input_selection,
            spatial_dimension
        ),
        "parameters": _get_default_parameters(
            fun_mod,
            param_selection,
            spatial_dimension,
        ),
    }

    return default_args


def create_from_default(
    fun_name: str,
    spatial_dimension: int = None,
    input_selection: str = None,
    param_selection: str = None,
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
    input_selection : str, optional
        When applicable, the keyword for selecting the input specification of
        a test function. Some test functions may be delivered with different
        input specifications based on the available literature.
        With 'None', the default will be used; if the selection is not
        available, the function returns an error.
    param_selection : str, optional
        When applicable, the keyword for selecting the parameters set of
        a test function. Some test functions may have different parameter values
        based on the available literature.
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
        input_selection,
        param_selection,
    )

    return UQTestFun(**default_args)


def _get_default_input(
    fun_module: ModuleType,
    selection: str = None,
    spatial_dimension: int = None
) -> dict:
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

    # Get the default dimension
    if spatial_dimension is None:
        spatial_dimension = _get_spatial_dimension(fun_module)
    else:
        _verify_spatial_dimension(spatial_dimension, fun_module)

    if selection is None:
        selection = fun_module.DEFAULT_INPUT_SELECTION

    # Check if the selection is valid
    if selection not in fun_module.DEFAULT_INPUTS:
        raise ValueError(
            f"Selected input specification ('{selection}') is not available!\n"
            f"Either specify 'None' (use the default) or one of "
            f"{list(fun_module.DEFAULT_INPUTS.keys())} \n"
            f"for the '{fun_module.DEFAULT_NAME}' test function."
        )

    default_input = fun_module.DEFAULT_INPUTS[selection]

    if isinstance(default_input, Callable):
        return default_input(spatial_dimension)

    return default_input


def _get_default_parameters(
    fun_module: ModuleType,
    selection: str = None,
    spatial_dimension: int = None
) -> tuple:
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

    # Get the default dimension
    if spatial_dimension is None:
        spatial_dimension = _get_spatial_dimension(fun_module)
    else:
        _verify_spatial_dimension(spatial_dimension, fun_module)

    if fun_module.DEFAULT_PARAMETERS is None:
        if selection is not None:
            raise ValueError(
                f"There is only one parametrization of "
                f"the '{fun_module.DEFAULT_NAME}' test function."
            )

        return None

    if selection is None:
        selection = fun_module.DEFAULT_PARAMETERS_SELECTION

    # Check if the selection is valid
    if selection not in fun_module.DEFAULT_PARAMETERS:
        raise ValueError(
            f"Selected parameters ('{selection}') is not available!\n"
            f"Either specify 'None' (use the default) or one of "
            f"{list(fun_module.DEFAULT_PARAMETERS.keys())} \n"
            f"for the '{fun_module.DEFAULT_NAME}' test function."
        )

    default_parameters = fun_module.DEFAULT_PARAMETERS[selection]

    if isinstance(default_parameters, Callable):
        default_parameters =  default_parameters(spatial_dimension)

    return default_parameters


def _get_spatial_dimension(fun_module: ModuleType) -> int:
    """Get the default spatial dimension specified at the module-level.

    Parameters
    ----------
    fun_module : ModuleType
        The module in which a test function was implemented.

    Returns
    -------
    int
        The spatial dimension as specified in the module.
    """
    if fun_module.SPATIAL_DIMENSION == None:
        spatial_dimension = fun_module.DEFAULT_DIMENSION
    else:
        spatial_dimension = fun_module.SPATIAL_DIMENSION

    return spatial_dimension


def _verify_spatial_dimension(spatial_dimension: int, fun_module: ModuleType):
    """Verify the specified spatial dimension given the default.

    Parameters
    ----------
    spatial_dimension : int
        The user-specified spatial dimension.
    fun_module : ModuleType
        The module in which a test function was implemented.
        The information regarding default dimension is stored therein.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the user-specified dimension is not consistent with the dimension
        stored in the module.
    """

    fun_name = fun_module.DEFAULT_NAME
    default_spatial_dimension = fun_module.SPATIAL_DIMENSION

    if default_spatial_dimension is not None:
        assert spatial_dimension == default_spatial_dimension,\
            f"The spatial dimension for the '{fun_name}' test function "\
            f"is fixed to {default_spatial_dimension} "\
            f"(but specified {spatial_dimension})."
