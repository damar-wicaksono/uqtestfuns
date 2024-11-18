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

from uqtestfuns.core.custom_typing import (
    MarginalSpecs,
    ProbInputSpecs,
    FunParamSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC


__all__ = ["Portfolio3D"]


MARGINALS_SALTELLI2004: MarginalSpecs = [
    {
        "name": "Ps",
        "distribution": "normal",
        "parameters": [0.0, 4.0],
        "description": "Hedged portfolio 's' [\N{euro sign}]",
    },
    {
        "name": "Pt",
        "distribution": "normal",
        "parameters": [0.0, 2.0],
        "description": "Hedged portfolio 't' [\N{euro sign}]",
    },
    {
        "name": "Pj",
        "distribution": "normal",
        "parameters": [0.0, 1.0],
        "description": "Hedged portfolio 'j' [\N{euro sign}]",
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Saltelli2004": {
        "function_id": "Portfolio3D",
        "description": (
            "Probabilistic input model for the simple portfolio model "
            "from Saltelli et al. (2004)."
        ),
        "marginals": MARGINALS_SALTELLI2004,
        "copulas": None,
    },
}

AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Saltelli2004-1": {
        "function_id": "Portfolio3D",
        "description": (
            "Parameter set for the simple 3D portfolio model from "
            "Saltelli et al. (2004); the least volatile hedged portfolio is "
            "the largest quantity"
        ),
        "declared_parameters": [
            {
                "keyword": "cs",
                "value": 100.0,
                "type": float,
                "description": "Quantities of the portfolio 's'",
            },
            {
                "keyword": "ct",
                "value": 500.0,
                "type": float,
                "description": "Quantities of the portfolio 't'",
            },
            {
                "keyword": "cj",
                "value": 1000.0,
                "type": float,
                "description": "Quantities of the portfolio 'j'",
            },
        ],
    },
    "Saltelli2004-2": {
        "function_id": "Portfolio3D",
        "description": (
            "Parameter set for the simple 3D portfolio model from "
            "Saltelli et al. (2004); the same quantities are hold for each "
            "hedged portfolio"
        ),
        "declared_parameters": [
            {
                "keyword": "cs",
                "value": 300.0,
                "type": float,
                "description": "Quantities of the portfolio 's'",
            },
            {
                "keyword": "ct",
                "value": 300.0,
                "type": float,
                "description": "Quantities of the portfolio 't'",
            },
            {
                "keyword": "cj",
                "value": 300.0,
                "type": float,
                "description": "Quantities of the portfolio 'j'",
            },
        ],
    },
    "Saltelli2004-3": {
        "function_id": "Portfolio3D",
        "description": (
            "Parameter set for the simple 3D portfolio model from "
            "Saltelli et al. (2004); the most volatile hedged portfolio is"
            "the largest quantity"
        ),
        "declared_parameters": [
            {
                "keyword": "cs",
                "value": 500.0,
                "type": float,
                "description": "Quantities of the portfolio 's'",
            },
            {
                "keyword": "ct",
                "value": 400.0,
                "type": float,
                "description": "Quantities of the portfolio 't'",
            },
            {
                "keyword": "cj",
                "value": 100.0,
                "type": float,
                "description": "Quantities of the portfolio 'j'",
            },
        ],
    },
}

DEFAULT_PARAMETERS_SELECTION = "Saltelli2004-1"


def evaluate(xx: np.ndarray, cs: float, ct: float, cj: float) -> np.ndarray:
    """Evaluate the simple portfolio model on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Three-Dimensional input values given by an ``(N, 3)`` array where
        ``N`` is the number of input values.
    cs : float
        The quantities of the portfolio 's' (the most volatile).
    ct : float
        The quantities of the portfolio 't' (average volatility).
    cj : float
        The quantities of the portfolio 'j' (the least volatile).

    Returns
    -------
    np.ndarray
        The output of the simple portfolio model on the given input values.
        The output is a one-dimensional array of length ``N``.
    """
    # Read the parameters
    p = np.array([cs, ct, cj])

    # Compute the simple portfolio model
    yy = np.sum(p * xx, axis=1)

    return yy


class Portfolio3D(UQTestFunFixDimABC):
    """An implementation of the simple portfolio model test function."""

    _tags = ["sensitivity"]
    _description = "Simple portfolio model from Saltelli et al. (2004)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = DEFAULT_PARAMETERS_SELECTION

    evaluate = staticmethod(evaluate)  # type: ignore
