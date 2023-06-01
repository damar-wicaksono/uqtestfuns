"""
Module with an implementation of the McLain's test functions.

The McLain's test functions consists of five two-dimensional scalar-valued
functions. The functions were introduced in [1] in the context of drawing
contours from a given set of points.

There are five test functions in McLain's paper each models a mathematically
defined surface:

- S5: A plateau and plain separated by a steep cliff

Four of the functions (S2-S5) appeared in modified forms in [2].

References
----------

1. D. H. McLain, "Drawing contours from arbitrary data points," The Computer
   Journal, vol. 17, no. 4, pp. 318-324, 1974.
   DOI: 10.1093/comjnl/17.4.318
2. Richard Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, Canada,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
"""
import numpy as np

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["McLainS5"]

INPUT_MARGINALS_MCLAIN1974 = [  # From Ref. [1]
    UnivDist(
        name="X1",
        distribution="uniform",
        parameters=[1.0, 10.0],
    ),
    UnivDist(
        name="X2",
        distribution="uniform",
        parameters=[1.0, 10.0],
    ),
]

AVAILABLE_INPUT_SPECS = {
    "McLain1974": {
        "name": "McLain-1974",
        "description": (
            "Input specification for the McLain's test functions "
            "from McLain (1974)."
        ),
        "marginals": INPUT_MARGINALS_MCLAIN1974,
        "copulas": None,
    }
}

DEFAULT_INPUT_SELECTION = "McLain1974"


class McLainS5(UQTestFunABC):
    """A concrete implementation of the McLain S5 function."""

    _TAGS = ["metamodeling"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = 2

    _DESCRIPTION = "McLain S5 function from McLain (1974)"

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        name: Optional[str] = None,
        rng_seed_prob_input: Optional[int] = None,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection,
            AVAILABLE_INPUT_SPECS,
            rng_seed=rng_seed_prob_input,
        )
        # Process the default name
        if name is None:
            name = McLainS5.__name__

        super().__init__(prob_input=prob_input, name=name)

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S5 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S5 function evaluated
            on the input values.
            The output is a 1-dimensional array of length N.
        """
        # Compute the (second) Franke function
        yy = np.tanh(xx[:, 0] + xx[:, 1] - 11)

        return yy
