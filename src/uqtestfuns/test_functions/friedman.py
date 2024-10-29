"""
Module with an implementation of the Friedman test functions.

The Friedman function is a function introduced in [2] as a six-dimensional
(including one dummy variable) test function for testing a spline approximation
method. It was later modified to be a ten-dimensional (including five dummy
variables) function in [2].
In [3], the function was employed as a test function in the context of
sensitivity analysis.

References
----------

1. J. H. Friedman, E. Grosse, and W. Stuetzle, "Multidimensional additive
   spline approximation," SIAM Journal on Scientific and Statistical Computing,
   vol. 4, no. 2, pp. 291-301, 1983.
2. J. H. Friedman, "Multivariate adaptive regression splines," The Annals of
   Statistics, vol. 19, no. 1, pp. 1-67, 1991.
   DOI: 10.1214/aos/1176347963
3. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental
   Modelling & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Friedman6D", "Friedman10D"]


AVAILABLE_INPUT_SPECS_6D = {
    "Friedman1983": ProbInputSpecFixDim(
        name="Friedman1983",
        description=(
            "Input specification for the 6D test function "
            "from Friedman et al. (1983)"
        ),
        marginals=[
            UnivDistSpec(
                name=f"x_{i + 1}",
                distribution="uniform",
                parameters=[0, 1],
                description="None",
            )
            for i in range(6)
        ],
        copulas=None,
    ),
}


AVAILABLE_INPUT_SPECS_10D = {
    "Friedman1983": ProbInputSpecFixDim(
        name="Friedman1991",
        description=(
            "Input specification for the 6D test function "
            "from Friedman (1991)"
        ),
        marginals=[
            UnivDistSpec(
                name=f"x_{i + 1}",
                distribution="uniform",
                parameters=[0, 1],
                description="None",
            )
            for i in range(10)
        ],
        copulas=None,
    ),
}


def evaluate_friedman(xx: np.ndarray) -> np.ndarray:
    """Evaluate the six-dimensional Friedman test function.

    Parameters
    ----------
    xx : np.ndarray
        6-Dimensional input values given by an N-by-6 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the six-dimensional Friedman function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy_1 = 10 * np.sin(np.pi * xx[:, 0] * xx[:, 1])
    yy_2 = 20 * (xx[:, 2] - 0.5) ** 2
    yy_3 = 10 * xx[:, 3]
    yy_4 = 5 * xx[:, 5]

    return yy_1 + yy_2 + yy_3 + yy_4


class Friedman6D(UQTestFunABC):
    """A concrete implementation of the 6D Friedman et al. (1983) function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Six-dimensional function from Friedman et al. (1983)"
    _available_inputs = AVAILABLE_INPUT_SPECS_6D
    _available_parameters = None
    _default_spatial_dimension = 6

    evaluate = staticmethod(evaluate_friedman)  # type: ignore


class Friedman10D(UQTestFunABC):
    """A concrete implementation of the 10D Friedman (1991) function."""

    _tags = ["metamodeling"]
    _description = "Ten-dimensional function from Friedman (1991)"
    _available_inputs = AVAILABLE_INPUT_SPECS_10D
    _available_parameters = None
    _default_spatial_dimension = 10

    evaluate = staticmethod(evaluate_friedman)  # type: ignore
