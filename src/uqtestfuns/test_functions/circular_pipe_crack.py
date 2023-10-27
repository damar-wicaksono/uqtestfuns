"""
Module with an implementation of the circular pipe crack reliability problem.

The two-dimensional reliability problem was introduced in [1] and used,
for instance, in [2].

The system under consideration is as a circular pipe with a circumferential
through-wall crack under a bending moment.
If the value of the performance function is negative,
then the system is in failed state.

References
----------
1. A. K. Verma, S. Ajit, and D. R. Karanki, “Structural Reliability,”
   in Reliability and Safety Engineering, in Springer Series
   in Reliability Engineering. London: Springer London, 2016, pp. 257–292.
   DOI: 10.1007/978-1-4471-6269-8_8
2. X. Li, C. Gong, L. Gu, W. Gao, Z. Jing, and H. Su, “A sequential surrogate
   method for reliability analysis based on radial basis function,”
   Structural Safety, vol. 73, pp. 42–53, 2018.
   DOI: 10.1016/j.strusafe.2018.02.005
"""
import numpy as np

from typing import Tuple

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC


__all__ = ["CircularPipeCrack"]


AVAILABLE_INPUT_SPECS = {
    "Verma2015": ProbInputSpecFixDim(
        name="CircularPipeCrack-Verma2015",
        description=(
            "Input model for the circular pipe crack problem "
            "from Verma et al. (2015)"
        ),
        marginals=[
            UnivDistSpec(
                name="sigma_f",
                distribution="normal",
                parameters=[301.079, 14.78],
                description="flow stress [MNm]",
            ),
            UnivDistSpec(
                name="theta",
                distribution="normal",
                parameters=[0.503, 0.049],
                description="half crack angle [-]",
            ),
        ],
        copulas=None,
    ),
}

AVAILABLE_PARAMETERS = {
    "Verma2016": (
        3.377e-1,  # Radius of the pipe [m]
        3.377e-2,  # Thickness of the pipe [m]
        3.0,  # Applied bending moment [Nm]
    ),
}


def evaluate(
    xx: np.ndarray, parameters: Tuple[float, float, float]
) -> np.ndarray:
    """Evaluate the circular pipe crack reliability on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by N-by-2 arrays
        where N is the number of input values.
    parameters : Tuple[float, float, float]
        The parameters of the test function, namely (and in the following
        order) the radius of the pipe, the thickness of the pipe,
        and the applied bending moment.

    Returns
    -------
    np.ndarray
        The performance evaluation of the circular pipe reliability.
        If negative, then the system is in failed state.
        The output is a one-dimensional array of length N.
    """
    # Get parameters
    pipe_radius, pipe_thickness, bending_moment = parameters

    # NOTE: Convert the flow stress from [MNm] to [Nm]
    yy = (
        4
        * pipe_thickness
        * xx[:, 0]
        * pipe_radius**2
        * (np.cos(xx[:, 1] / 2) - 0.5 * np.sin(xx[:, 1]))
        - bending_moment
    )

    return yy


class CircularPipeCrack(UQTestFunABC):
    """A concrete implementation of the circular pipe crack problem."""

    _tags = ["reliability"]
    _description = (
        "Circular pipe under bending moment from Verma et al. (2015)"
    )
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate)
