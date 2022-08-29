"""

"""
from . import wing_weight


def get_default_args(fun_name: str):

    fun_name = fun_name.lower()

    if fun_name == "wing weight":
        mod_name = wing_weight
    else:
        raise ValueError("Test function name is not supported!")

    default_args = {
        "name": mod_name.DEFAULT_NAME,
        "evaluate": mod_name.evaluate,
        "input": mod_name.DEFAULT_INPUT,
        "parameters": mod_name.DEFAULT_PARAMETERS
    }

    return default_args
