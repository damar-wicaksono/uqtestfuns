"""
Module with an implementation of the four-branch test function.

The two-dimensional four-branch function introduced in [1] is a reliability
benchmark problem (see, for instance, [2], [3], [4], [5]).
The test function describes the failure of a series system with four distinct
performance function parts.

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


def evaluate(xx: np.ndarray, p: float) -> np.ndarray:
    """Evaluate the four-branch function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 2)`` array of input values where ``N`` is the number of
        evaluation points.
    p : float
        The parameter of the test function; a single float.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the function output.
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
