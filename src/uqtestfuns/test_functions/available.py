"""
Helpers module to construct probabilistic input and parameters.
"""
from types import FunctionType
from typing import Any, Dict, Optional, Union
from ..core import ProbInput
from ..core.prob_input.input_spec import ProbInputSpec, ProbInputSpecVarDim


def create_parameters_from_available(
    param_selection: Optional[str],
    available_parameters: dict,
    spatial_dimension: Optional[int] = None,
) -> Any:
    """Construct a set of parameters given available specifications.

    Parameters
    ----------
    param_selection : str
        Which parameter specification to construct.
    available_parameters : dict
        Dictionary of available parameters specifications.
    spatial_dimension : int, optional
        The requested number of spatial dimensions, when applicable.
        Some specifications are functions of spatial dimension.
    """

    if param_selection is None:
        return None

    if param_selection in available_parameters:
        parameters = available_parameters[param_selection]
        if isinstance(parameters, FunctionType):
            parameters = parameters(spatial_dimension)
    else:
        raise ValueError("Invalid parameters selection!")

    return parameters


def get_prob_input_spec(
    prob_input_selection: Optional[str],
    available_input_specs: Dict[str, ProbInputSpec],
) -> Optional[ProbInputSpec]:
    """Get ProbInputSpec from the available specifications.

    Parameters
    ----------
    """
    if prob_input_selection is None:
        return None

    if prob_input_selection in available_input_specs:
        prob_input_spec = available_input_specs[prob_input_selection]
    else:
        raise KeyError("Invalid ProbInput selection!")

    return prob_input_spec


def create_prob_input_from_spec(
    prob_input_spec: Optional[Union[ProbInputSpec, ProbInputSpecVarDim]],
    spatial_dimension: Optional[int] = None,
    rng_seed: Optional[int] = None,
) -> Optional[ProbInput]:
    """Construct a Multivariate input given available specifications.

    Parameters
    ----------
    prob_input_spec : Union[ProbInputSpec, ProbInputSpecVarDim], optional
        The specification of a probabilistic input model.
    spatial_dimension : int, optional
        The requested number of spatial dimensions, when applicable.
        Some specifications are functions of spatial dimension.
    rng_seed : int, optional
        The seed for the pseudo-random number generator; if not given then
        the number is taken from the system entropy.
    """
    if prob_input_spec is None:
        return None

    prob_input = ProbInput.from_spec(
        prob_input_spec, spatial_dimension=spatial_dimension, rng_seed=rng_seed
    )

    return prob_input
