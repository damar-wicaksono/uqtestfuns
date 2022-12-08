"""
Module with an implementation of the Wing Weight test function.

The Wing Weight test function[1] is a 10-dimensional scalar-valued function
that models a light aircraft wing.

References
----------

1. A. I. J. Forrester, A. Sóbester, and A. J. Keane, Engineering Design
   via Surrogate Modelling: A Practical Guide, 1st ed. Wiley, 2008.
   doi: 10.1002/9780470770801.
"""
import numpy as np

from .utils import deg2rad

DEFAULT_NAME = "Wing-Weight"

DEFAULT_INPUT_DICTS = [
    {
        "name": "Sw",
        "distribution": "uniform",
        "parameters": [150, 200],
        "description": "wing area [ft^2]",
    },
    {
        "name": "Wfw",
        "distribution": "uniform",
        "parameters": [220, 300],
        "description": "weight of fuel in the wing [lb]",
    },
    {
        "name": "A",
        "distribution": "uniform",
        "parameters": [6, 10],
        "description": "aspect ratio [-]",
    },
    {
        "name": "Lambda",
        "distribution": "uniform",
        "parameters": [-10, 10],
        "description": "quarter-chord sweep [degrees]",
    },
    {
        "name": "q",
        "distribution": "uniform",
        "parameters": [16, 45],
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

DEFAULT_INPUTS = {
    "forrester": DEFAULT_INPUT_DICTS,
}

DEFAULT_INPUT_SELECTION = "forrester"

DEFAULT_PARAMETERS = None

SPATIAL_DIMENSION = len(DEFAULT_INPUT_DICTS)


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
        The output of the Wing Weight function evaluated on the input values.
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
