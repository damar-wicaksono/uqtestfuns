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
from ..core import UnivariateInput

DEFAULT_NAME = "Wing-Weight"

TAGS = ["metamodeling", "sensitivity-analysis"]


INPUT_MARGINALS_FORRESTER = [
    UnivariateInput(
        name="Sw",
        distribution="uniform",
        parameters=[150.0, 200.0],
        description="wing area [ft^2]",
    ),
    UnivariateInput(
        name="Wfw",
        distribution="uniform",
        parameters=[220.0, 300.0],
        description="weight of fuel in the wing [lb]",
    ),
    UnivariateInput(
        name="A",
        distribution="uniform",
        parameters=[6.0, 10.0],
        description="aspect ratio [-]",
    ),
    UnivariateInput(
        name="Lambda",
        distribution="uniform",
        parameters=[-10.0, 10.0],
        description="quarter-chord sweep [degrees]",
    ),
    UnivariateInput(
        name="q",
        distribution="uniform",
        parameters=[16.0, 45.0],
        description="dynamic pressure at cruise [lb/ft^2]",
    ),
    UnivariateInput(
        name="lambda",
        distribution="uniform",
        parameters=[0.5, 1.0],
        description="taper ratio [-]",
    ),
    UnivariateInput(
        name="tc",
        distribution="uniform",
        parameters=[0.08, 0.18],
        description="aerofoil thickness to chord ratio [-]",
    ),
    UnivariateInput(
        name="Nz",
        distribution="uniform",
        parameters=[2.5, 6.0],
        description="ultimate load factor [-]",
    ),
    UnivariateInput(
        name="Wdg",
        distribution="uniform",
        parameters=[1700, 2500],
        description="flight design gross weight [lb]",
    ),
    UnivariateInput(
        name="Wp",
        distribution="uniform",
        parameters=[0.025, 0.08],
        description="paint weight [lb/ft^2]",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "forrester": {
        "name": "Wing-Weight-Forrester",
        "description": (
            "Probabilistic input model for the Wing Weight model "
            "from Forrester et al. (2008)."
        ),
        "marginals": INPUT_MARGINALS_FORRESTER,
        "copulas": None,
    }
}

DEFAULT_INPUT_SELECTION = "forrester"

AVAILABLE_PARAMETERS = None


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
