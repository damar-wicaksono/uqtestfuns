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

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["Piston"]

# Marginals specification from [1]
INPUT_MARGINALS_BENARI2007 = [
    UnivDist(
        name="M",
        distribution="uniform",
        parameters=[30.0, 60.0],
        description="Piston weight [kg]",
    ),
    UnivDist(
        name="S",
        distribution="uniform",
        parameters=[0.005, 0.020],
        description="Piston surface area [m^2]",
    ),
    UnivDist(
        name="V0",
        distribution="uniform",
        parameters=[0.002, 0.010],
        description="Initial gas volume [m^3]",
    ),
    UnivDist(
        name="k",
        distribution="uniform",
        parameters=[1000.0, 5000.0],
        description="Spring coefficient [N/m]",
    ),
    UnivDist(
        name="P0",
        distribution="uniform",
        parameters=[90000.0, 110000.0],
        description="Atmospheric pressure [N/m^2]",
    ),
    UnivDist(
        name="Ta",
        distribution="uniform",
        parameters=[290.0, 296.0],
        description="Ambient temperature [K]",
    ),
    UnivDist(
        name="T0",
        distribution="uniform",
        parameters=[340.0, 360.0],
        description="Filling gas temperature [K]",
    ),
]

# Marginals specification from [2]
INPUT_MARGINALS_MOON2010 = [copy(_) for _ in INPUT_MARGINALS_BENARI2007]
for i in range(13):
    INPUT_MARGINALS_MOON2010.append(
        UnivDist(
            name=f"Inert {i+1}",
            distribution="uniform",
            parameters=[100.0, 200.0],
            description="Inert input [-]",
        )
    )

AVAILABLE_INPUT_SPECS = {
    "BenAri2007": {
        "name": "Piston-Ben-Ari-2007",
        "description": (
            "Probabilistic input model for the Piston simulation model "
            "from Ben-Ari and Steinberg (2007)."
        ),
        "marginals": INPUT_MARGINALS_BENARI2007,
        "copulas": None,
    },
    "Moon2010": {
        "name": "Piston-Moon-2010",
        "description": (
            "Probabilistic input model for the Piston simulation model "
            "from Moon (2010)."
        ),
        "marginals": INPUT_MARGINALS_MOON2010,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "BenAri2007"


class Piston(UQTestFunABC):
    """A concrete implementation of the Piston simulation test function."""

    _TAGS = ["metamodeling", "sensitivity"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = 7

    _DESCRIPTION = "Piston simulation model from Ben-Ari and Steinberg (2007)"

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
            name = Piston.__name__

        super().__init__(prob_input=prob_input, name=name)

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
        mm = xx[:, 0]  # piston weight
        ss = xx[:, 1]  # piston surface area
        vv_0 = xx[:, 2]  # initial gas volume
        kk = xx[:, 3]  # spring coefficient
        pp_0 = xx[:, 4]  # atmospheric pressure
        tt_a = xx[:, 5]  # ambient temperature
        tt_0 = xx[:, 6]  # filling gas temperature

        # Compute the force
        aa = pp_0 * ss + 19.62 * mm - kk * vv_0 / ss

        # Compute the force difference
        daa = np.sqrt(aa**2 + 4.0 * kk * pp_0 * vv_0 * tt_a / tt_0) - aa

        # Compute the volume difference
        vv = ss / 2.0 / kk * daa

        # Compute the cycle time
        cc = (
            2.0
            * np.pi
            * np.sqrt(
                mm / (kk + ss**2 * pp_0 * vv_0 * tt_a / tt_0 / vv**2)
            )
        )

        return cc
