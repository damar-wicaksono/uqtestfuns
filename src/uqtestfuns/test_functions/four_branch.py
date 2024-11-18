"""
Module with an implementation of the four-branch test function.

The two-dimensional four-branch function introduced in [1] is a reliability
benchmark problem (see, for instance, [2], [3], [4], [5]).
The test function describes the failure of a series system with four distinct
performance function components.

References
----------

1. Satoshi Katsuki and Dan M. Frangopol, “Hyperspace division method for
   structural Reliability,” Journal of  Engineering Mechanic, vol. 120, no. 11,
   pp. 2405–2427, 1994.
   DOI: 10.1061/(ASCE)0733-9399(1994)120:11(2405)
2. Paul Hendrik Waarts, “Structural reliability using finite element
   analysis - an appraisal of DARS: Directional adaptive response surface
   sampling," Civil Engineering and Geosciences, TU Delft, Delft,
   The Netherlands, 2000.
3. Luc Schueremans and Dionys Van Gemert, “Benefit of splines and neural
   networks in simulation based structural reliability analysis,” Structural
   Safety, vol. 27, no. 3, pp. 246–261, 2005.
   DOI: 10.1016/j.strusafe.2004.11.001
4. B. Echard, N. Gayton, and M. Lemaire, “AK-MCS: An active learning
   reliability method combining Kriging and Monte Carlo Simulation,”
   Structural Safety, vol. 33, no. 2, pp. 145–154, 2011.
   DOI: 10.1016/j.strusafe.2011.01.002
5. Roland Schöbi, Bruno Sudret, and Stefano Marelli, “Rare event estimation
   using polynomial-chaos kriging,” ASCE-ASME Journal Risk and Uncertainty
   in Engineering System, Part A: Civil Engineering, vol. 3, no. 2,
   p. D4016002, 2017.
   DOI: 10.1061/AJRUA6.0000870.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["FourBranch"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Katsuki1994": {
        "function_id": "FourBranch",
        "description": (
            "Input model for the four-branch function "
            "from Katsuki and Frangopol (1994)"
        ),
        "marginals": [
            {
                "name": "X1",
                "distribution": "normal",
                "parameters": [0, 1],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "normal",
                "parameters": [0, 1],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Katsuki1994": {
        "function_id": "FourBranch",
        "description": (
            "Parameter set for the Four-branch function from Katsuki and "
            "Frangopol (1994)"
        ),
        "declared_parameters": [
            {
                "keyword": "p",
                "value": 3.5 * np.sqrt(2),
                "type": float,
                "description": None,
            },
        ],
    },
    "Schueremans2005": {
        "function_id": "FourBranch",
        "description": (
            "Parameter set for the Four-branch function from Schueremans "
            "(2005)"
        ),
        "declared_parameters": [
            {
                "keyword": "p",
                "value": 6.0 / np.sqrt(2),
                "type": float,
                "description": None,
            },
        ],
    },
}


def evaluate(xx: np.ndarray, p: float) -> np.ndarray:
    """Evaluate the four-branch function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-Dimensional input values given by an N-by-2 array
        where N is the number of input values.
    p : float
        The parameter of the test function; a single float.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    # Compute the performance function components
    yy_1 = (
        3.0
        + 0.1 * (xx[:, 0] - xx[:, 1]) ** 2
        - (xx[:, 0] + xx[:, 1]) / np.sqrt(2)
    )
    yy_2 = (
        3.0
        + 0.1 * (xx[:, 0] - xx[:, 1]) ** 2
        + (xx[:, 0] + xx[:, 1]) / np.sqrt(2)
    )
    yy_3 = xx[:, 0] - xx[:, 1] + p
    yy_4 = -1 * xx[:, 0] + xx[:, 1] + p

    yy = np.vstack((yy_1, yy_2, yy_3, yy_4))

    return np.min(yy, axis=0)


class FourBranch(UQTestFunFixDimABC):
    """A concrete implementation of the four-branch test function."""

    _tags = ["reliability"]
    _description = (
        "Series system reliability from Katsuki and Frangopol (1994)"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = "Schueremans2005"

    evaluate = staticmethod(evaluate)  # type: ignore
