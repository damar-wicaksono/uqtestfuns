"""
Module with an implementation of the Quadratic RS reliability problem.

The two-dimensional function is a variant of the classic RS reliability problem
with one quadratic term [1].

References
----------
1. Paul Hendrik Waarts, “Structural reliability using finite element
   analysis - an appraisal of DARS: Directional adaptive response surface
   sampling," Civil Engineering and Geosciences, TU Delft, Delft,
   The Netherlands, 2000.
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["RSQuadratic"]

AVAILABLE_INPUT_SPECS = {
    "Waarts2000": ProbInputSpecFixDim(
        name="RSQuadratic-Waarts2000",
        description="Input model for the quadratic RS from Waarts (2000)",
        marginals=[
            UnivDistSpec(
                name="X1",
                distribution="normal",
                parameters=[11.0, 1.0],
                description="None",
            ),
            UnivDistSpec(
                name="X2",
                distribution="normal",
                parameters=[1.5, 0.5],
                description="None",
            ),
        ],
        copulas=None,
    ),
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the quadratic RS function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The performance function of the problem.
        If negative, the system is in failed state.
        The output is a one-dimensional array of length N.
    """

    # Compute the performance function
    yy = xx[:, 0] - xx[:, 1] ** 2

    return yy


class RSQuadratic(UQTestFunABC):
    """Concrete implementation of the quadratic RS reliability problem."""

    _tags = ["reliability"]
    _description = "RS problem w/ one quadratic term from Waarts (2000)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = None
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate)
