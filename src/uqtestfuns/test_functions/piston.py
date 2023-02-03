"""
Module with an implementation of the Piston simulation test function.

The Piston simulation test function is a seven-dimensional scalar-valued
test function.
The function computes the cycle time of a piston.
The function has been used as a test function in metamodeling exercises [1].
A 20-dimensional variant was used for sensitivity analysis in [2]
by introducing 13 additional inert input variables.

References
----------

1. E. N. Ben-Ari and D. M. Steinberg, "Modeling data from computer
   experiments: An empirical comparison of Kriging with MARS
   and projection pursuit regression," Quality Engineering,
   vol. 19, pp. 327-338, 2007.
   DOI: 10.1080/08982110701580930
2. H. Moon, "Design and Analysis of Computer Experiments for Screening Input
   Variables," Ph. D. dissertation, Ohio State University, Ohio, 2010.
   URL: http://rave.ohiolink.edu/etdc/view?acc_num=osu1275422248
"""
import numpy as np

from copy import copy
from typing import Optional

from ..core.prob_input.univariate_input import UnivariateInput
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["Piston"]

# Marginals specification from [1]
INPUT_MARGINALS_BEN_ARI = [
    UnivariateInput(
        name="M",
        distribution="uniform",
        parameters=[30.0, 60.0],
        description="Piston weight [kg]",
    ),
    UnivariateInput(
        name="S",
        distribution="uniform",
        parameters=[0.005, 0.020],
        description="Piston surface area [m^2]",
    ),
    UnivariateInput(
        name="V0",
        distribution="uniform",
        parameters=[0.002, 0.010],
        description="Initial gas volume [m^3]",
    ),
    UnivariateInput(
        name="k",
        distribution="uniform",
        parameters=[1000.0, 5000.0],
        description="Spring coefficient [N/m]",
    ),
    UnivariateInput(
        name="P0",
        distribution="uniform",
        parameters=[90000.0, 110000.0],
        description="Atmospheric pressure [N/m^2]",
    ),
    UnivariateInput(
        name="Ta",
        distribution="uniform",
        parameters=[290.0, 296.0],
        description="Ambient temperature [K]",
    ),
    UnivariateInput(
        name="T0",
        distribution="uniform",
        parameters=[340.0, 360.0],
        description="Filling gas temperature [K]",
    ),
]

# Marginals specification from [2]
INPUT_MARGINALS_MOON = [copy(_) for _ in INPUT_MARGINALS_BEN_ARI]
for i in range(13):
    INPUT_MARGINALS_MOON.append(
        UnivariateInput(
            name=f"Inert {i+1}",
            distribution="uniform",
            parameters=[100.0, 200.0],
            description="Inert input [-]",
        )
    )

AVAILABLE_INPUT_SPECS = {
    "ben-ari": {
        "name": "Piston-Ben-Ari",
        "description": (
            "Probabilistic input model for the Piston simulation model "
            "from Ben-Ari and Steinberg (2007)."
        ),
        "marginals": INPUT_MARGINALS_BEN_ARI,
        "copulas": None,
    },
    "moon": {
        "name": "Piston-Moon",
        "description": (
            "Probabilistic input model for the Piston simulation model "
            "from Moon (2010)."
        ),
        "marginals": INPUT_MARGINALS_MOON,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "ben-ari"


class Piston(UQTestFunABC):
    """A concrete implementation of the Piston simulation test function."""

    tags = ["metamodeling", "sensitivity-analysis"]

    available_inputs = tuple(AVAILABLE_INPUT_SPECS.keys())

    available_parameters = None

    default_dimension = 7

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )

        super().__init__(prob_input=prob_input, name=Piston.__name__)

    def evaluate(self, xx: np.ndarray) -> np.ndarray:
        """Evaluate the OTL circuit test function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            (At least) 6-dimensional input values given by N-by-6 arrays
            where N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the OTL circuit test function,
            i.e., the mid-point voltage in Volt.
            The output is a one-dimensional array of length N.

        Notes
        -----
        - The variant of this test function has 14 additional inputs,
          but they are all taken to be inert and therefore should not affect
          the output.
        """
        rr_b1 = xx[:, 0]  # Resistance b1
        rr_b2 = xx[:, 1]  # Resistance b2
        rr_f = xx[:, 2]  # Resistance f
        rr_c1 = xx[:, 3]  # Resistance c1
        rr_c2 = xx[:, 4]  # Resistance c2
        beta = xx[:, 5]  # Current gain

        # Compute the voltage across b1
        vb1 = 12 * rr_b1 / (rr_b1 + rr_b2)

        # Compute the mid-point voltage
        denom = beta * (rr_c2 + 9) + rr_f
        term_1 = ((vb1 + 0.74) * beta * (rr_c2 + 9)) / denom
        term_2 = 11.35 * rr_f / denom
        term_3 = 0.74 * rr_f * beta * (rr_c2 + 9) / (rr_c1 * denom)

        vm = term_1 + term_2 + term_3

        return vm
