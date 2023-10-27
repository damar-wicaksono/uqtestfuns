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

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Piston"]

# Marginals specification from [1]
INPUT_MARGINALS_BENARI2007 = [
    UnivDistSpec(
        name="M",
        distribution="uniform",
        parameters=[30.0, 60.0],
        description="Piston weight [kg]",
    ),
    UnivDistSpec(
        name="S",
        distribution="uniform",
        parameters=[0.005, 0.020],
        description="Piston surface area [m^2]",
    ),
    UnivDistSpec(
        name="V0",
        distribution="uniform",
        parameters=[0.002, 0.010],
        description="Initial gas volume [m^3]",
    ),
    UnivDistSpec(
        name="k",
        distribution="uniform",
        parameters=[1000.0, 5000.0],
        description="Spring coefficient [N/m]",
    ),
    UnivDistSpec(
        name="P0",
        distribution="uniform",
        parameters=[90000.0, 110000.0],
        description="Atmospheric pressure [N/m^2]",
    ),
    UnivDistSpec(
        name="Ta",
        distribution="uniform",
        parameters=[290.0, 296.0],
        description="Ambient temperature [K]",
    ),
    UnivDistSpec(
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
        UnivDistSpec(
            name=f"Inert {i+1}",
            distribution="uniform",
            parameters=[100.0, 200.0],
            description="Inert input [-]",
        )
    )

AVAILABLE_INPUT_SPECS = {
    "BenAri2007": ProbInputSpecFixDim(
        name="Piston-BenAri2007",
        description=(
            "Probabilistic input model for the Piston simulation model "
            "from Ben-Ari and Steinberg (2007)."
        ),
        marginals=INPUT_MARGINALS_BENARI2007,
        copulas=None,
    ),
    "Moon2010": ProbInputSpecFixDim(
        name="Piston-Moon2010",
        description=(
            "Probabilistic input model for the Piston simulation model "
            "from Moon (2010)."
        ),
        marginals=INPUT_MARGINALS_MOON2010,
        copulas=None,
    ),
}

DEFAULT_INPUT_SELECTION = "BenAri2007"


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Piston simulation test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        (At least) 6-dimensional input values given by N-by-6 arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Piston simulation test function,
        The output is a one-dimensional array of length N.

    Notes
    -----
    - The variant of this test function has 13 additional inputs,
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
        * np.sqrt(mm / (kk + ss**2 * pp_0 * vv_0 * tt_a / tt_0 / vv**2))
    )

    return cc


class Piston(UQTestFunABC):
    """A concrete implementation of the Piston simulation test function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Piston simulation model from Ben-Ari and Steinberg (2007)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = None
    _default_spatial_dimension = 7
    _default_input = DEFAULT_INPUT_SELECTION

    eval_ = staticmethod(evaluate)
