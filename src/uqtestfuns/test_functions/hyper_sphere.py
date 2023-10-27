"""
Module with an implementation of the hyper-sphere bound reliability problem.

The reliability problem is a two-dimensional function as described in
Li et al. (2018).

References
----------

1. X. Li, C. Gong, L. Gu, W. Gao, Z. Jing, and H. Su, “A sequential surrogate
   method for reliability analysis based on radial basis function,”
   Structural Safety, vol. 73, pp. 42–53, 2018.
   DOI: 10.1016/j.strusafe.2018.02.005.
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["HyperSphere"]


AVAILABLE_INPUT_SPECS = {
    "Li2018": ProbInputSpecFixDim(
        name="Li2018",
        description=(
            "Input model for the hyper-sphere reliability problem "
            "from Li et al. (2018)"
        ),
        marginals=[
            UnivDistSpec(
                name="X1",
                distribution="normal",
                parameters=[0.5, 0.2],
                description="None",
            ),
            UnivDistSpec(
                name="X2",
                distribution="normal",
                parameters=[0.5, 0.2],
                description="None",
            ),
        ],
        copulas=None,
    ),
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the hyper-sphere performance function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 1 - xx[:, 0] ** 3 - xx[:, 1] ** 3

    return yy


class HyperSphere(UQTestFunABC):
    """A concrete implementation of the hyper-sphere reliability problem."""

    _tags = ["reliability"]
    _description = (
        "Hyper-sphere bound reliability problem from Li et al. (2018)"
    )
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = None
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate)
