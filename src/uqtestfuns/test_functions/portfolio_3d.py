"""
Module with an implementation of the simple 3D portfolio model.

The simple portfolio model is a three-dimensional scalar-valued function.
The function was first introduced in [1] as an example for illustrating
different sensitivity measures (i.e., local and hybrid-local).

References
----------

1. A. Saltelli, S. Tarantola, F. Campolongo, M. Rattom, "Sensitivity analysis
   in practice: a guide to assessing scientific models," Hoboken, NJ: Wiley,
   2004.
"""

import numpy as np

from typing import Tuple

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Portfolio3D"]


INPUT_MARGINALS_SALTELLI2004 = [
    UnivDistSpec(
        name="Ps",
        distribution="normal",
        parameters=[0.0, 4.0],
        description="Hedged portfolio 's' [\N{euro sign}]",
    ),
    UnivDistSpec(
        name="Pt",
        distribution="normal",
        parameters=[0.0, 2.0],
        description="Hedged portfolio 't' [\N{euro sign}]",
    ),
    UnivDistSpec(
        name="Pj",
        distribution="normal",
        parameters=[0.0, 1.0],
        description="Hedged portfolio 'j' [\N{euro sign}]",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "Saltelli2004": ProbInputSpecFixDim(
        name="Portfolio3D-Saltelli2004",
        description=(
            "Probabilistic input model for the simple portfolio model "
            "from Saltelli et al. (2004)."
        ),
        marginals=INPUT_MARGINALS_SALTELLI2004,
        copulas=None,
    ),
}

AVAILABLE_PARAMETERS = {
    "Saltelli2004a": (100.0, 500.0, 1000.0),  # from [1]
    "Saltelli2004b": (300.0, 300.0, 300.0),  # from [1]
    "Saltelli2004c": (500.0, 400.0, 100.0),  # from [1]
}

DEFAULT_PARAMETERS_SELECTION = "Saltelli2004a"


def evaluate(xx: np.ndarray, parameters: Tuple[float, float, float]):
    """Evaluate the simple portfolio model on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Three-Dimensional input values given by an ``(N, 3)`` array where
        ``N`` is the number of input values.
    parameters : Tuple[float, float, float]
        Tuple of three values as the parameters of the function (i.e.,
        the quantities per hedged portfolio).

    Returns
    -------
    np.ndarray
        The output of the simple portfolio model on the given input values.
        The output is a one-dimensional array of length ``N``.
    """
    # Read the parameters
    p = np.array(parameters)

    # Compute the simple portfolio model
    yy = np.sum(p * xx, axis=1)

    return yy


class Portfolio3D(UQTestFunABC):
    """An implementation of the simple portfolio model test function."""

    _tags = ["sensitivity"]
    _description = "Simple portfolio model from Saltelli et al. (2004)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters = DEFAULT_PARAMETERS_SELECTION
    _default_spatial_dimension = 3

    eval_ = staticmethod(evaluate)
