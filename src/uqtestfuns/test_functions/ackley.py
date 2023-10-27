"""
Module with an implementation of the M-dimensional Ackley function.

The Ackley function  is an $M$-dimensional scalar-valued function.
The function was first introduced in [1] as a test function for optimization
algorithms,
Originally presented as a two-dimensional function, it was later generalized
by Bäck and Schwefel [2].

References
----------

1. D. H. Ackley, A Connectionist Machine for Genetic Hillclimbing,
   The Kluwer International Series in Engineering and Computer Science vol. 28.
   Boston, MA: Springer US, 1987.
   DOI: 10.1007/978-1-4613-1997-9
2. T. Bäck and H.-P. Schwefel, “An overview of evolutionary algorithms for
   parameter optimization,” Evolutionary Computation,
   vol. 1, no. 1, pp. 1–23, 1993.
   DOI: 10.1162/evco.1993.1.1.1.
"""
import numpy as np

from typing import List, Tuple

from ..core.uqtestfun_abc import UQTestFunABC
from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecVarDim

__all__ = ["Ackley"]


def _ackley_input(spatial_dimension: int) -> List[UnivDistSpec]:
    """Create a list of marginals for the M-dimensional Ackley function.

    Parameters
    ----------
    spatial_dimension : int
        The requested spatial dimension of the probabilistic input model.

    Returns
    -------
    List[UnivDistSpec]
        A list of marginals for the multivariate input following Ref. [1]
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivDistSpec(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[-32.768, 32.768],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "Ackley1987": ProbInputSpecVarDim(
        name="Ackley1987",
        description=(
            "Search domain for the Ackley function from Ackley (1987)."
        ),
        marginals_generator=_ackley_input,
        copulas=None,
    ),
}

AVAILABLE_PARAMETERS = {"Ackley1987": np.array([20, 0.2, 2 * np.pi])}


def evaluate(xx: np.ndarray, parameters: Tuple[float, float, float]):
    """Evaluate the Ackley function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    parameters : Tuple[float, float, float]
        A tuple of length 3 for the parameters of the Ackley function.

    Returns
    -------
    np.ndarray
        The output of the Ackley function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    m = xx.shape[1]
    a, b, c = parameters

    # Compute the Ackley function
    term_1 = -1 * a * np.exp(-1 * b * np.sqrt(np.sum(xx**2, axis=1) / m))
    term_2 = -1 * np.exp(np.sum(np.cos(c * xx), axis=1) / m)

    yy = term_1 + term_2 + a + np.exp(1)

    return yy


class Ackley(UQTestFunABC):
    """A concrete implementation of the M-dimensional Ackley test function."""

    _tags = ["optimization", "metamodeling"]
    _description = "Optimization test function from Ackley (1987)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_spatial_dimension = None  # Indicate that this is variable dim.

    eval_ = staticmethod(evaluate)
