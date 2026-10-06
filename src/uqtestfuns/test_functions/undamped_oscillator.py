"""
Module with an implementation of undamped oscillator test function.

The undamped oscillator function is a six-dimensional, scalar-valued test
function that models a non-linear, undamped, single-degree-of-freedom, forced
oscillating mechanical system.
This function is frequently used as a test function for reliability analysis
methods (see [1] through [6]). It is also used in [7] as a test function
for metamodeling exercises

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
7. N. Lüthen, S. Marelli, and B. Sudret, “Sparse Polynomial Chaos Expansions:
   Literature Survey and Benchmark,” SIAM/ASA Journal of Uncertainty
   Quantification, vol. 9, no. 2, pp. 593–649, 2021.
   DOI: 10.1137/20M1315774
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the undamped oscillator test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 6)`` array of input values,
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
