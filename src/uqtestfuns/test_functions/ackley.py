"""
Module with an implementation of the M-dimensional Ackley function.

The Ackley function [1] is an M-dimensional non-convex scalar-valued function
typically used for testing optimization algorithms.
Originally, the function is presented as a two-dimensional function.

References
----------

1. D. H. Ackley, "A connectionist machine for genetic hillclimbing."
   Boston, MA:  Kluwer Academic Publishers, 1987.
"""
import numpy as np

from typing import List, Optional

from ..core.uqtestfun_abc import UQTestFunABC
from ..core.prob_input.univariate_input import UnivariateInput
from .available import (
    create_prob_input_from_available,
    create_parameters_from_available,
)

__all__ = ["Ackley"]


def _ackley_input(spatial_dimension: int) -> List[UnivariateInput]:
    """Create a list of marginals for the M-dimensional Ackley function.

    Parameters
    ----------
    spatial_dimension : int
        The requested spatial dimension of the probabilistic input model.

    Returns
    -------
    List[UnivariateInput]
        A list of marginals for the multivariate input following Ref. [1]
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivariateInput(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[-32.768, 32.768],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "ackley": {
        "name": "Ackley",
        "description": (
            "Probabilistic input model for the Ackley function "
            "from Ackley (1987)."
        ),
        "marginals": _ackley_input,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "ackley"

AVAILABLE_PARAMETERS = {"ackley": (20, 0.2, 2 * np.pi)}

DEFAULT_PARAMETERS_SELECTION = "ackley"

# The dimension is variable so define a default for fallback
DEFAULT_DIMENSION_SELECTION = 2


class Ackley(UQTestFunABC):
    """A concrete implementation of the M-dimensional Ackley test function.

    Parameters
    ----------
    spatial_dimension : int
        The requested number of spatial_dimension. If not specified,
        the default is set to 2.
    prob_input_selection : str, optional
        The selection of a probabilistic input model from a list of
        available specifications. This is a keyword only parameter.
    parameters_selection : str, optional
        The selection of a parameters sets from a list of available
        parameter sets. This is a keyword only parameter.
    """

    tags = ["optimization"]

    available_inputs = tuple(AVAILABLE_INPUT_SPECS.keys())

    available_parameters = tuple(AVAILABLE_PARAMETERS.keys())

    default_dimension = None

    def __init__(
        self,
        spatial_dimension: int = DEFAULT_DIMENSION_SELECTION,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        parameters_selection: Optional[str] = DEFAULT_PARAMETERS_SELECTION,
    ):
        # --- Arguments processing
        if not isinstance(spatial_dimension, int):
            raise TypeError(
                f"Spatial dimension is expected to be of 'int'. "
                f"Got {type(spatial_dimension)} instead."
            )
        # Ackley is an M-dimensional test function, either given / use default
        # Create the input according to spatial dimension
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS, spatial_dimension
        )
        # Create the parameters according to spatial dimension
        parameters = create_parameters_from_available(
            parameters_selection, AVAILABLE_PARAMETERS, spatial_dimension
        )

        super().__init__(
            prob_input=prob_input, parameters=parameters, name=Ackley.__name__
        )

    def evaluate(self, xx: np.ndarray):
        """Evaluate the Ackley function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            M-Dimensional input values given by an N-by-M array where
            N is the number of input values.
        params : tuple
            A tuple of length 3 for the parameters of the Ackley function.

        Returns
        -------
        np.ndarray
            The output of the Ackley function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """

        m = xx.shape[1]
        a, b, c = self.parameters

        # Compute the Ackley function
        term_1 = -1 * a * np.exp(-1 * b * np.sqrt(np.sum(xx**2, axis=1) / m))
        term_2 = -1 * np.exp(np.sum(np.cos(c * xx), axis=1) / m)

        yy = term_1 + term_2 + a + np.exp(1)

        return yy
