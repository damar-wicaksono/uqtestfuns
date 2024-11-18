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

from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC


__all__ = ["CircularPipeCrack"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Verma2015": {
        "function_id": "CircularPipeCrack",
        "description": (
            "Input model for the circular pipe crack problem "
            "from Verma et al. (2015)"
        ),
        "marginals": [
            {
                "name": "sigma_f",
                "distribution": "normal",
                "parameters": [301.079, 14.78],
                "description": "flow stress [MNm]",
            },
            {
                "name": "theta",
                "distribution": "normal",
                "parameters": [0.503, 0.049],
                "description": "half crack angle [-]",
            },
        ],
        "copulas": None,
    },
}

AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Verman2016": {
        "function_id": "CircularPipeCrack",
        "description": (
            "Parameter set for the circular pipe crack reliability problem "
            "from Verma et al. (2016)"
        ),
        "declared_parameters": [
            {
                "keyword": "pipe_radius",
                "value": 3.377e-1,
                "type": float,
                "description": "Radius of the pipe [m]",
            },
            {
                "keyword": "pipe_thickness",
                "value": 3.377e-2,
                "type": float,
                "description": "Thickness of the pipe [m]",
            },
            {
                "keyword": "bending_moment",
                "value": 3.0,
                "type": float,
                "description": "Applied bending moment [Nm]",
            },
        ],
    },
}


def evaluate(
    xx: np.ndarray,
    pipe_radius: float,
    pipe_thickness: float,
    bending_moment: float,
) -> np.ndarray:
    """Evaluate the circular pipe crack reliability on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by N-by-2 arrays
        where N is the number of input values.
    pipe_radius : float
        The radius of the pipe in [m].
    pipe_thickness : float
        The thickness of the pipe in [m].
    bending_moment : float
        The applied bending moment in [Nm].

    Returns
    -------
    np.ndarray
        The performance evaluation of the circular pipe reliability.
        If negative, then the system is in failed state.
        The output is a one-dimensional array of length N.
    """
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


class CircularPipeCrack(UQTestFunFixDimABC):
    """A concrete implementation of the circular pipe crack problem."""

    _tags = ["reliability"]
    _description = (
        "Circular pipe under bending moment from Verma et al. (2015)"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS

    evaluate = staticmethod(evaluate)  # type: ignore
