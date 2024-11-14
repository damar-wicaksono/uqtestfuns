"""
Module with an implementation of undamped oscillator test function.

The undamped oscillator function is a six-dimensional, scalar-valued test
function that models a non-linear, undamped, single-degree-of-freedom, forced
oscillating mechanical system.
This function is frequently used as a test function for reliability analysis
methods (see [1] through [6]). Additionally, in [7], the function is employed
as a test function for metamodeling exercises.


1. C. G. Bucher and U. Bourgund, “A fast and efficient response surface
   approach for structural reliability problems,” Structural Safety, vol. 7,
   no. 1, pp. 57–66, 1990.
   DOI: 10.1016/0167-4730(90)90012-E
2. M. R. Rajashekhar and B. R. Ellingwood, “A new look at the response surface
   approach for reliability analysis,” Structural Safety, vol. 12, no. 3,
   pp. 205–220, 1993.
   DOI: 10.1016/0167-4730(93)90003-J
3. N. Gayton, J. M. Bourinet, and M. Lemaire, “CQ2RS: a new statistical
   approach to the response surface method for reliability analysis,”
   Structural Safety, vol. 25, no. 1, pp. 99–121, 2003.
   DOI: 10.1016/S0167-4730(02)00045-0
4. L. Schueremans and D. Van Gemert, “Benefit of splines and neural networks
   in simulation based structural reliability analysis,” Structural Safety,
   vol. 27, no. 3, pp. 246–261, 2005.
   DOI: 10.1016/j.strusafe.2004.11.001
5. B. Echard, N. Gayton, and M. Lemaire, “AK-MCS: An active learning
   reliability method combining Kriging and Monte Carlo Simulation,”
   Structural Safety, vol. 33, no. 2, pp. 145–154, 2011.
   DOI: 10.1016/j.strusafe.2011.01.002.
6. B. Echard, N. Gayton, M. Lemaire, and N. Relun, “A combined Importance
   Sampling and Kriging reliability method for small failure probabilities
   with time-demanding numerical models,” Reliability Engineering &
   System Safety, vol. 111, pp. 232–240, 2013.
   DOI: 10.1016/j.ress.2012.10.008.
8. N. Lüthen, S. Marelli, and B. Sudret, “Sparse Polynomial Chaos Expansions:
   Literature Survey and Benchmark,” SIAM/ASA Journal of Uncertainty
   Quantification, vol. 9, no. 2, pp. 593–649, 2021.
   DOI: 10.1137/20M1315774
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC


__all__ = ["UndampedOscillator"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Gayton2003": {
        "function_id": "UndampedOscillator",
        "description": (
            "Input model for the undamped non-linear oscillator "
            "from Gayton et al. (2003) (Table 9)"
        ),
        "marginals": [
            {
                "name": "m",
                "distribution": "normal",
                "parameters": [1.0, 0.05],
                "description": "Mass",
            },
            {
                "name": "c1",
                "distribution": "normal",
                "parameters": [1.0, 0.10],
                "description": "Spring (1) constant",
            },
            {
                "name": "c2",
                "distribution": "normal",
                "parameters": [0.1, 0.01],
                "description": "Spring (2) constant",
            },
            {
                "name": "r",
                "distribution": "normal",
                "parameters": [0.5, 0.05],
                "description": "Length of restoring force",
            },
            {
                "name": "F1",
                "distribution": "normal",
                "parameters": [1.0, 0.2],
                "description": "Pulse load",
            },
            {
                "name": "t1",
                "distribution": "normal",
                "parameters": [1.0, 0.2],
                "description": "Duration of the pulse load",
            },
        ],
        "copulas": None,
    },
    "Echard2013-1": {
        "function_id": "UndampedOscillator",
        "description": (
            "Input model for the undamped non-linear oscillator "
            "from Echard et al. (2013) (Table 4, F1 = 0.6)"
        ),
        "marginals": [
            {
                "name": "m",
                "distribution": "normal",
                "parameters": [1.0, 0.05],
                "description": "Mass",
            },
            {
                "name": "c1",
                "distribution": "normal",
                "parameters": [1.0, 0.10],
                "description": "Spring (1) constant",
            },
            {
                "name": "c2",
                "distribution": "normal",
                "parameters": [0.1, 0.01],
                "description": "Spring (2) constant",
            },
            {
                "name": "r",
                "distribution": "normal",
                "parameters": [0.5, 0.05],
                "description": "Length of restoring force",
            },
            {
                "name": "F1",
                "distribution": "normal",
                "parameters": [0.6, 0.1],
                "description": "Pulse load",
            },
            {
                "name": "t1",
                "distribution": "normal",
                "parameters": [1.0, 0.2],
                "description": "Duration of the pulse load",
            },
        ],
        "copulas": None,
    },
    "Echard2013-2": {
        "function_id": "UndampedOscillator",
        "description": (
            "Input model for the undamped non-linear oscillator "
            "from Echard et al. (2013) (Table 4, F1 = 0.45)"
        ),
        "marginals": [
            {
                "name": "m",
                "distribution": "normal",
                "parameters": [1.0, 0.05],
                "description": "Mass",
            },
            {
                "name": "c1",
                "distribution": "normal",
                "parameters": [1.0, 0.10],
                "description": "Spring (1) constant",
            },
            {
                "name": "c2",
                "distribution": "normal",
                "parameters": [0.1, 0.01],
                "description": "Spring (2) constant",
            },
            {
                "name": "r",
                "distribution": "normal",
                "parameters": [0.5, 0.05],
                "description": "Length of restoring force",
            },
            {
                "name": "F1",
                "distribution": "normal",
                "parameters": [0.45, 0.45 / 6],
                "description": "Pulse load",
            },
            {
                "name": "t1",
                "distribution": "normal",
                "parameters": [1.0, 0.2],
                "description": "Duration of the pulse load",
            },
        ],
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the undamped oscillator test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by N-by-6 arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        If negative, then the system is in failed state.
        The output is a 1-dimensional array of length N.
    """
    omega_0 = np.sqrt((xx[:, 1] + xx[:, 2]) / xx[:, 0])
    term_1 = 3 * xx[:, 3]
    term_2 = 2 * xx[:, 4] / xx[:, 0] / omega_0**2
    term_3 = np.sin(omega_0 * xx[:, 5] / 2)

    yy = term_1 - np.abs(term_2 * term_3)

    return yy


class UndampedOscillator(UQTestFunFixDimABC):
    """A concrete implementation of the undamped oscillator test function."""

    _tags = ["reliability", "metamodeling"]
    _description = "Undamped, non-linear, single DOF oscillator"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None
    _default_input_id = "Gayton2003"

    evaluate = staticmethod(evaluate)  # type: ignore
