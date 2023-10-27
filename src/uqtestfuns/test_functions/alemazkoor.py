"""
Module with an implementation of Alemazkoor & Meidani (2008) test functions.

There are two test functions from [1].
One features a low-dimensional polynomial function with a high degree
(a total degree of 20).

The functions were used as test functions
for a metamodeling exercise (i.e., sparse polynomial chaos expansion) in [1].

References
----------

1. Negin Alemazkoor and Hadi Meidani, "A near-optimal sampling strategy for
   sparse recovery of polynomial chaos expansions," Journal of Computational
   Physics, vol. 371, pp. 137-151, 2018.
   DOI: 10.1016/j.jcp.2018.05.025
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Alemazkoor2D"]

AVAILABLE_INPUT_SPECS_2D = {
    "Alemazkoor2018": ProbInputSpecFixDim(
        name="2D-Alemazkoor2018",
        description=(
            "Input specification for the 2D test function "
            "from Alemazkoor & Meidani (2018)"
        ),
        marginals=[
            UnivDistSpec(
                name="X1",
                distribution="uniform",
                parameters=[-1, 1],
                description="None",
            ),
            UnivDistSpec(
                name="X2",
                distribution="uniform",
                parameters=[-1, 1],
                description="None",
            ),
        ],
        copulas=None,
    ),
}


def evaluate_2d(xx: np.ndarray) -> np.ndarray:
    """The evaluation for the Alemazkoor & Meidani (2018) 2D function.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.zeros(xx.shape[0])

    for i in range(1, 6):
        yy += xx[:, 0] ** (2 * i) * xx[:, 1] ** (2 * i)

    return yy


class Alemazkoor2D(UQTestFunABC):
    """An implementation of the 2D function of Alemazkoor & Meidani (2018)."""

    _tags = ["metamodeling"]
    _description = (
        "Two-dimensional high-degree polynomial from Alemazkoor "
        "& Meidani (2018)"
    )
    _available_inputs = AVAILABLE_INPUT_SPECS_2D
    _available_parameters = None
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate_2d)
