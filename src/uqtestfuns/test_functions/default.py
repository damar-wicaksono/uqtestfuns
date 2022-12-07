"""
Module that exposes top-level functionalities to create default test functions.

A default function means that the input specification, parameters, and
spatial dimension (when applicable) used to create the funciton are taken from
the built-in default values.
"""
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


def get_default_args(fun_name: str, spatial_dimension: int = None) -> dict:
    """Get the arguments to instantiate a UQTestFun from the default selection.

    Parameters
    ----------
    fun_name : str
        Test function name, it must be already registered in the module-level
        constant ``AVAILABLE_FUNCTIONS``.

    Returns
    -------
    dict
        A dictionary to construct an instance of UQTestFun using the default
        setting for the selected test function.
    """

    fun_name = fun_name.lower()

    fun_mod = AVAILABLE_FUNCTIONS[fun_name]

    default_args = {
        "name": fun_mod.DEFAULT_NAME,
        "evaluate": fun_mod.evaluate,
        "input": fun_mod.get_default_input(spatial_dimension),
        "parameters": fun_mod.DEFAULT_PARAMETERS,
    }

    return default_args


def create_from_default(
        fun_name: str,
        spatial_dimension: int = None,
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

    Returns
    -------
    UQTestFun
        An instance of UQTestFun created using the default setting for the
        selected test function.
    """
    default_args = get_default_args(fun_name, spatial_dimension)

    return UQTestFun(**default_args)
