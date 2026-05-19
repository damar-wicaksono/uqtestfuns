"""
Module with an implementation of the damped oscillator base model.

The damped oscillator base model is a seven-dimensional scalar-valued
function that computes the root-mean-square relative displacement of
the secondary spring under a white noise base acceleration.

The base model is based on a two-degree-of-freedom primary-secondary
mechanical system characterized by two masses, two springs, and the
corresponding damping ratios.

References
----------
1. Takeru Igusa and Armen Der Kiureghian, "Dynamic characterization of
   two-degree-of-freedom equipment-structure systems,"
   Journal of Engineering Mechanics, vol. 111, no. 1, pp. 1-19, 1985.
   DOI: 10.1061/(ASCE)0733-9399(1985)111:1(1)
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the damped oscillator model.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 7)`` array of input values.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the
        root-mean-square relative displacement of the secondary spring.
    """

    # Get the parameters
    mm_p = xx[:, 0]  # Primary mass
    mm_s = xx[:, 1]  # Secondary mass
    kk_p = xx[:, 2]  # Primary spring stiffness
    kk_s = xx[:, 3]  # Secondary spring stiffness
    zt_p = xx[:, 4]  # Damping ratio of the primary damper
    zt_s = xx[:, 5]  # Damping ratio of the secondary damper
    ss_0 = xx[:, 6]  # White noise base acceleration intensity

    # Compute natural frequencies
    omega_p = np.sqrt(kk_p / mm_p)  # Primary system
    omega_s = np.sqrt(kk_s / mm_s)  # Secondary system

    # Compute additional parameters
    gamma = mm_s / mm_p  # relative mass
    omega_a = (omega_p + omega_s) / 2.0  # average natural frequency
    zt_a = (zt_p + zt_s) / 2.0  # average damping ratio
    theta = (omega_p - omega_s) / omega_a  # tuning parameter

    # Compute the RMS relative displacement of the secondary spring
    first_term = np.pi * ss_0 / 4 / zt_s / (omega_s**3)
    second_term = (
        zt_a
        * zt_s
        / (zt_p * zt_s * (4 * zt_a**2 + theta**2) + gamma * zt_a**2)
    )
    third_term = (
        (zt_p * omega_p**3 + zt_s * omega_s**3)
        * omega_p
        / 4
        / zt_a
        / (omega_a**4)
    )

    # NOTE: This is squared displacement
    xx_s = first_term * second_term * third_term

    return np.sqrt(xx_s)
