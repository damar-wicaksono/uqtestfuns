"""
Module with an implementation of the 1D Oakley-O'Hagan test function.

The 1D Oakley-O'Hagan test function is a one-dimensional scalar-valued
function. It was used in [1] as a test function for illustrating metamodeling
and uncertainty propagation approaches.

References
----------

1. Jeremy Oakley and Anthony O'Hagan, "Bayesian inference for the uncertainty
   distribution of computer model outputs," Biometrika , Vol. 89, No. 4,
   p. 769-784, 2002.
   DOI: 10.1093/biomet/89.4.769
"""
import numpy as np

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["OakleyOHagan1D"]

INPUT_MARGINALS_OAKLEY2002 = [
    UnivDist(
        name="x",
        distribution="normal",
        parameters=[0.0, 4.0],
        description="None",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "Oakley2002": {
        "name": "Oakley-OHagan-2002",
        "description": (
            "Probabilistic input model for the one-dimensional function "
            "from Oakley-O'Hagan function (2002)"
        ),
        "marginals": INPUT_MARGINALS_OAKLEY2002,
    }
}

DEFAULT_INPUT_SELECTION = "Oakley2002"


class OakleyOHagan1D(UQTestFunABC):
    """A concrete implementation of the 1D Oakley-O'Hagan test function."""

    _TAGS = ["metamodeling"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = 1

    _DESCRIPTION = "One-dimensional function from Oakley and O'Hagan (2002)"

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        name: Optional[str] = None,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )
        # Process the default name
        if name is None:
            name = OakleyOHagan1D.__name__

        super().__init__(prob_input=prob_input, name=name)

    def evaluate(self, xx: np.ndarray):
        """Evaluate the 1D Oakley-O'Hagan function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            1-Dimensional input values given by an N-by-1 array
            where N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the 1D Oakley-O'Hagan function evaluated
            on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = 5 + xx + np.cos(xx)

        return yy
