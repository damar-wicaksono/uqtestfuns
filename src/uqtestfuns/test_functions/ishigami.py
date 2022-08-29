"""
Module with an implementation of the Ishigami function.

The Ishigami test function[1] is a 3-dimensional scalar-valued function.
It is a highly non-linear and non-monotonic function.

References
----------

1. T. Ishigami and T. Homma, “An importance quantification technique in
   uncertainty analysis for computer models,” in [1990] Proceedings.
   First International Symposium on Uncertainty Modeling and Analysis,
   College Park, MD, USA, 1991, pp. 398–403. doi: 10.1109/ISUMA.1990.151285.
2. I. M. Sobol’ and Y. L. Levitan, “On the use of variance reducing multipliers
   in Monte Carlo computations of a global sensitivity index,”
   Computer Physics Communications, vol. 117, no. 1, pp. 52–61, 1999.
   DOI:10.1016/S0010-4655(98)00156-8
"""
import numpy as np

from ..core import MultivariateInput
from .utils import verify_input

DEFAULT_NAME = "Ishigami"

DEFAULT_INPUT_DICTS = [
    {
        "name": "X1",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": "None"
    },
    {
        "name": "X2",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": "None"
    },
    {
        "name": "X2",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": "None"
    }
]

DEFAULT_INPUT = MultivariateInput(DEFAULT_INPUT_DICTS)

# The parameter set is from [2].
DEFAULT_PARAMETERS = (7, 0.05)


def evaluate(xx: np.ndarray, params: tuple = DEFAULT_PARAMETERS) -> np.ndarray:
    """Evaluate the Ishigami function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        3-Dimensional input values given by N-by-3 arrays where
        N is the number of input values.
    params : tuple
        Tuple of two values as the parameters of the function.

    Returns
    -------
    np.ndarray
        The output of the Ishigami function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    # Verify the shape of the input
    verify_input(xx, DEFAULT_INPUT.spatial_dimension)

    # Compute the Ishigami function
    term_1 = np.sin(xx[:, 0])
    term_2 = params[0] * np.sin(xx[:, 1])**2
    term_3 = params[1] * xx[:, 2]**4 * np.sin(xx[:, 0])

    yy = term_1 + term_2 + term_3

    return yy
