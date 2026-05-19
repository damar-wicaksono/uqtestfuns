"""
Module with an implementation of the damped oscillator reliability problem.

The R-S damped oscillator reliability problem is an eight-dimensional
reliability analysis test function. The performance function is the force
capacity of the secondary spring minus the peak force, where the peak
force is the product of the peak factor, the secondary spring stiffness,
and the root-mean-square relative displacement computed
by the base damped oscillator model.

References
----------
1. Armen Der Kiureghian and Mario De Stefano, "An efficient algorithm for
   second-order reliability analysis," Department of Civil and Environmental
   Engineering, University of California, Berkeley, UCB/SEMM-90/20, 1990.
2. Armen Der Kiureghian and Mario De Stefano, "Efficient algorithm for
   second-order reliability analysis," Journal of Engineering Mechanics,
   vol. 117, no. 12, pp. 2904-2923, 1991.
   DOI: 10.1061/(ASCE)0733-9399(1991)117:12(2904)
3. J.-M. Bourinet, F. Deheeger, and M. Lemaire, "Assessing small failure
   probabilities by combined subset simulation and Support Vector Machines,"
   Structural Safety, vol. 33, no. 6, pp. 343-353, 2011.
   DOI: 10.1016/j.strusafe.2011.06.001
4. Vincent Dubourg, "Adaptive surrogate models for reliability analysis
   and reliability-based design optimization," Universite Blaise Pascal
   - Clermont II, Clermont-Ferrand, France, 2011.
   URL: https://sites.google.com/site/vincentdubourg/phd-thesis
"""

import numpy as np

from .damped_oscillator import evaluate as evaluate_base


def evaluate(xx: np.ndarray, pf: float):
    """Evaluate the performance function of the damped oscillator system.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 8)`` array of input values.
    pf : float
        The peak factor of the system.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N``. If less than or equal
        to zero, the system is in failed state.
    """
    # root-mean-square displacement
    rms_disp = evaluate_base(xx[:, :-1])
    # Secondary spring stiffness
    kk_s = xx[:, 3]
    # Force capacity of the secondary spring
    ff_s = xx[:, -1]

    # RS problem
    yy = ff_s - pf * kk_s * rms_disp

    return yy
