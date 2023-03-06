"""
Module with an implementation of the M-dimensional Ackley function.

The Ackley function  is an $M$-dimensional scalar-valued function.
The function was first introduced in [1] as a test function for optimization
algorithms,
Originally presented as a two-dimensional function, it was later generalized
by Bäck and Schwefel [2].

References
----------

1. D. H. Ackley, A Connectionist Machine for Genetic Hillclimbing,
   The Kluwer International Series in Engineering and Computer Science vol. 28.
   Boston, MA: Springer US, 1987.
   DOI: 10.1007/978-1-4613-1997-9
2. T. Bäck and H.-P. Schwefel, “An overview of evolutionary algorithms for
   parameter optimization,” Evolutionary Computation,
   vol. 1, no. 1, pp. 1–23, 1993.
   DOI: 10.1162/evco.1993.1.1.1.
"""
import numpy as np

from typing import List, Optional

from ..core.uqtestfun_abc import UQTestFunABC
from ..core.prob_input.univariate_distribution import UnivDist
from .available import (
    create_prob_input_from_available,
    create_parameters_from_available,
)

__all__ = ["Ackley"]


def _ackley_input(spatial_dimension: int) -> List[UnivDist]:
    """Create a list of marginals for the M-dimensional Ackley function.

    Parameters
    ----------
    spatial_dimension : int
        The requested spatial dimension of the probabilistic input model.

    Returns
    -------
    List[UnivDist]
        A list of marginals for the multivariate input following Ref. [1]
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivDist(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[-32.768, 32.768],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "Ackley1987": {
        "name": "Ackley-Ackley-1987",
        "description": (
            "Search domain for the Ackley function from Ackley (1987)."
        ),
        "marginals": _ackley_input,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "Ackley1987"

AVAILABLE_PARAMETERS = {"Ackley1987": np.array([20, 0.2, 2 * np.pi])}

DEFAULT_PARAMETERS_SELECTION = "Ackley1987"

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

    _TAGS = ["optimization", "metamodeling"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = tuple(AVAILABLE_PARAMETERS.keys())

    _DEFAULT_SPATIAL_DIMENSION = None

    _DESCRIPTION = "Ackley function from Ackley (1987)"

    def __init__(
        self,
        spatial_dimension: int = DEFAULT_DIMENSION_SELECTION,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        parameters_selection: Optional[str] = DEFAULT_PARAMETERS_SELECTION,
        name: Optional[str] = None,
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
        # Process the default name
        if name is None:
            name = Ackley.__name__

        super().__init__(
            prob_input=prob_input, parameters=parameters, name=name
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
