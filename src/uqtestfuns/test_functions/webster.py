"""
Module with an implementation of the 2D function from Webster et al. (1996).

The two-dimensional function is polynomial with random input variables.
It was introduced in [1] and used to illustrate the construction of polynomial
chaos expansion metamodel.

References
----------
1. M. Webster, M. A. Tatang, and G. J. McRae, “Application of the probabilistic
   collocation method for an uncertainty analysis of a simple ocean model,”
   Massachusetts Institute of Technology, Cambridge, MA,
   Joint Program Report Series 4, 1996.
   [Online]. Available: http://globalchange.mit.edu/publication/15670
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Webster2D"]


AVAILABLE_INPUT_SPECS = {
    "Webster1996": ProbInputSpecFixDim(
        name="Webster1996",
        description=(
            "Input specification for the 2D function "
            "from Webster et al. (1996)"
        ),
        marginals=[
            UnivDistSpec(
                name="A",
                distribution="uniform",
                parameters=[1.0, 10.0],
                description="None",
            ),
            UnivDistSpec(
                name="B",
                distribution="normal",
                parameters=[2.0, 1.0],
                description="None",
            ),
        ],
        copulas=None,
    ),
}


def evaluate(xx: np.ndarray):
    """Evaluate the 2D Webster function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 2D Webster function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = xx[:, 0] ** 2 + xx[:, 1] ** 3

    return yy


class Webster2D(UQTestFunABC):
    """A concrete implementation of the function from Webster et al. (1996)."""

    _tags = ["metamodeling"]
    _description = "2D polynomial function from Webster et al. (1996)."
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = None
    _default_spatial_dimension = 2

    eval_ = staticmethod(evaluate)
