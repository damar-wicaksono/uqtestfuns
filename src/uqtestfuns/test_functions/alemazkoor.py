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

__all__ = ["Alemazkoor2D", "Alemazkoor20D"]

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

AVAILABLE_INPUT_SPECS_20D = {
    "Alemazkoor2018": ProbInputSpecFixDim(
        name="20D-Alemazkoor2018",
        description=(
            "Input specification for the 20D test function "
            "from Alemazkoor & Meidani (2018)"
        ),
        marginals=[
            UnivDistSpec(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[-1, 1],
                description="None",
            )
            for i in range(20)
        ],
        copulas=None,
    )
}


def evaluate_2d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 2D test function from Alemazkoor & Meidani (2018).

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an ``(N, 2)`` array where
        ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a one-dimensional array of length ``N``.
    """
    yy = np.zeros(xx.shape[0])

    for i in range(1, 6):
        yy += xx[:, 0] ** (2 * i) * xx[:, 1] ** (2 * i)

    return yy


class Alemazkoor2D(UQTestFunABC):
    """An implementation of the 2D function of Alemazkoor & Meidani (2018)."""

    _tags = ["metamodeling"]
    _description = (
        "Low-dimensional high-degree polynomial from Alemazkoor "
        "& Meidani (2018)"
    )
    _available_inputs = AVAILABLE_INPUT_SPECS_2D
    _available_parameters = None
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate_2d)


def evaluate_20d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 20D test function from Alemazkoor & Meidani (2018).

    Parameters
    ----------
    xx : np.ndarray
        A 20-dimensional input values given by an ``(N, 20)`` array
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a one-dimensional array of length ``N``.
    """
    yy = np.sum(xx[:, :-1] * xx[:, 1:], axis=1)

    return yy


class Alemazkoor20D(UQTestFunABC):
    """An implementation of the 20D function of Alemazkoor & Meidani (2018)."""

    _tags = ["metamodeling"]
    _description = (
        "High-dimensional low-degree polynomial from Alemazkoor "
        "& Meidani (2018)"
    )
    _available_inputs = AVAILABLE_INPUT_SPECS_20D
    _available_parameters = None
    _default_spatial_dimension = 20

    eval_ = staticmethod(evaluate_20d)
