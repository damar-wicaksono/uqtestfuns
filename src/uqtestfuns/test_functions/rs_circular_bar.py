"""
Module with an implementation of the circular bar RS problem.

The two-dimensional function is a variant of the classic RS reliability problem
with one quadratic term [1].

References
----------
1. A. K. Verma, S. Ajit, and D. R. Karanki, “Structural Reliability,”
   in Reliability and Safety Engineering, in Springer Series
   in Reliability Engineering. London: Springer London, 2016, pp. 257–292.
   DOI: 10.1007/978-1-4471-6269-8_8
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["RSCircularBar"]

AVAILABLE_INPUT_SPECS = {
    "Verma2016": ProbInputSpecFixDim(
        name="RSCircularBar-Verma2016",
        description=(
            "Input model for the circular bar RS from Verma et al. (2016)"
        ),
        marginals=[
            UnivDistSpec(
                name="Y",
                distribution="normal",
                parameters=[250.0, 25.0],
                description="Material mean yield strength [MPa]",
            ),
            UnivDistSpec(
                name="F",
                distribution="normal",
                parameters=[70.0, 7.0],
                description="Force mean value [kN]",
            ),
        ],
        copulas=None,
    ),
}

AVAILABLE_PARAMETERS = {
    "Verma2016": 25,  # bar diameter in [mm]
}


def evaluate(xx: np.ndarray, parameter: float) -> np.ndarray:
    """Evaluate the circular bar RS problem on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.
    parameter : float
        The parameter of the function (i.e., the diameter of the bar in [mm]).

    Returns
    -------
    np.ndarray
        The performance function of the problem.
        If negative, the system is in failed state.
        The output is a one-dimensional array of length N.
    """
    # Convert to SI units
    yy_ = xx[:, 0] * 1e6  # From [MPa] to [Pa]
    ff = xx[:, 1] * 1e3  # From [kN] to [N]
    diam = parameter * 1e-3  # From [mm] to [m]

    # Compute the performance function
    yy = yy_ - ff / (np.pi * diam**2 / 4)

    return yy


class RSCircularBar(UQTestFunABC):
    """Concrete implementation of the circular bar RS reliability problem."""

    _tags = ["reliability"]
    _description = "RS problem as a circular bar from Verma et al. (2016)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate)
