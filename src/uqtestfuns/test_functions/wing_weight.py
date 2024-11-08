"""
Module with an implementation of the Wing Weight test function.

The Wing Weight test function [1] is a 10-dimensional scalar-valued function
that models a light aircraft wing.
The function has been used as a test function in the context of
metamodeling [2] and optimization [1].

References
----------

1. Alexander I. J. Forrester, András Sóbester, and Andy J. Keane,
   Engineering Design via Surrogate Modelling: A Practical Guide, 1st ed.
   Wiley, 2008.
   DOI: 10.1002/9780470770801.
2. Lavi R. Zuhal, Kemas Zakaria, Pramudita S. Palar, Koji Shimoyama,
   and Rhea P. Liem, "Gradient-enhanced universal Kriging with polynomial
   chaos as trend function," In AIAA Scitech 2020 Forum,
   Orlando, Florida, 2020. American Institute of Aeronautics and Astronautics.
   DOI: 10.2514/6.2020-1865.
"""

import numpy as np

from uqtestfuns.core.custom_typing import MarginalSpecs, ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC
from .utils import deg2rad

__all__ = ["WingWeight"]


MARGINALS_FORRESTER2008: MarginalSpecs = [
    {
        "name": "Sw",
        "distribution": "uniform",
        "parameters": [150.0, 200.0],
        "description": "wing area [ft^2]",
    },
    {
        "name": "Wfw",
        "distribution": "uniform",
        "parameters": [220.0, 300.0],
        "description": "weight of fuel in the wing [lb]",
    },
    {
        "name": "A",
        "distribution": "uniform",
        "parameters": [6.0, 10.0],
        "description": "aspect ratio [-]",
    },
    {
        "name": "Lambda",
        "distribution": "uniform",
        "parameters": [-10.0, 10.0],
        "description": "quarter-chord sweep [degrees]",
    },
    {
        "name": "q",
        "distribution": "uniform",
        "parameters": [16.0, 45.0],
        "description": "dynamic pressure at cruise [lb/ft^2]",
    },
    {
        "name": "lambda",
        "distribution": "uniform",
        "parameters": [0.5, 1.0],
        "description": "taper ratio [-]",
    },
    {
        "name": "tc",
        "distribution": "uniform",
        "parameters": [0.08, 0.18],
        "description": "aerofoil thickness to chord ratio [-]",
    },
    {
        "name": "Nz",
        "distribution": "uniform",
        "parameters": [2.5, 6.0],
        "description": "ultimate load factor [-]",
    },
    {
        "name": "Wdg",
        "distribution": "uniform",
        "parameters": [1700, 2500],
        "description": "flight design gross weight [lb]",
    },
    {
        "name": "Wp",
        "distribution": "uniform",
        "parameters": [0.025, 0.08],
        "description": "paint weight [lb/ft^2]",
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Forrester2008": {
        "function_id": "WingWeight",
        "description": (
            "Probabilistic input model for the Wing Weight model "
            "from Forrester et al. (2008)."
        ),
        "marginals": MARGINALS_FORRESTER2008,
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Wing Weight function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        10-Dimensional input values given by N-by-10 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Wing Weight function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    # Compute the Wing Weight function
    term_1 = 0.036 * xx[:, 0] ** 0.758 * xx[:, 1] ** 0.0035
    term_2 = (xx[:, 2] / np.cos(deg2rad(xx[:, 3])) ** 2) ** 0.6
    term_3 = xx[:, 4] ** 0.006
    term_4 = xx[:, 5] ** 0.04
    term_5 = (100 * xx[:, 6] / np.cos(np.pi / 180.0 * xx[:, 3])) ** (-0.3)
    term_6 = (xx[:, 7] * xx[:, 8]) ** 0.49
    term_7 = xx[:, 0] * xx[:, 9]

    yy = term_1 * term_2 * term_3 * term_4 * term_5 * term_6 + term_7

    return yy


class WingWeight(UQTestFunFixDimABC):
    """A concrete implementation of the wing weight test function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Wing weight model from Forrester et al. (2008)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
