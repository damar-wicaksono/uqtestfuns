"""
Module with an implementation of the damped oscillator model.

The damped oscillator model is a seven-dimensional scalar-valued function
that computes the relative displacement of a secondary spring
under a white noise base acceleration.
The model was first proposed in [1] and used in the context of reliability
analysis in [2] and [3]. Note, however, that the reliability analysis
variant differs from this base model.
Used in the context of reliability analysis,
the model also includes additional parameters related to a capacity factor and
load such that the performance function can be computed.

The damped oscillator model is based on a two-degree-of-freedom
primary-secondary mechanical system characterized by two masses, two springs,
and the corresponding damping ratios.

References
----------
1. Takeru Igusa and Armen Der Kiureghian, “Dynamic characterization of
   two‐degree‐of‐freedom equipment‐structure systems,”
   Journal of Engineering Mechanics, vol. 111, no. 1, pp. 1–19, 1985.
   DOI: 10.1061/(ASCE)0733-9399(1985)111:1(1)
2. Armen Der Kiureghian and Mario De Stefano, “Efficient algorithm for
   second‐order reliability analysis,” Journal of Engineering Mechanics,
   vol. 117, no. 12, pp. 2904–2923, 1991.
   DOI: 10.1061/(ASCE)0733-9399(1991)117:12(2904)
3. Vincent Dubourg, “Adaptive surrogate models for reliability analysis
   and reliability-based design optimization,”
   Université Blaise Pascal - Clermont II, Clermont-Ferrand, France, 2011.
   URL: https://sites.google.com/site/vincentdubourg/phd-thesis
"""
import numpy as np

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .utils import lognorm2norm_mean, lognorm2norm_std
from .available import create_prob_input_from_available

__all__ = ["DampedOscillator"]

INPUT_MARGINALS_DERKIUREGHIAN1991 = [  # From [2]
    UnivDist(
        name="Mp",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(1.5, 0.1 * 1.5),
            lognorm2norm_std(1.5, 0.1 * 1.5),
        ],
        description="Primary mass",
    ),
    UnivDist(
        name="Ms",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(0.01, 0.1 * 0.01),
            lognorm2norm_std(0.01, 0.1 * 0.01),
        ],
        description="Secondary mass",
    ),
    UnivDist(
        name="Kp",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(1.0, 0.2 * 1.0),
            lognorm2norm_std(1.0, 0.2 * 1.0),
        ],
        description="Primary spring stiffness",
    ),
    UnivDist(
        name="Ks",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(0.01, 0.2 * 0.01),
            lognorm2norm_std(0.01, 0.2 * 0.01),
        ],
        description="Secondary spring stiffness",
    ),
    UnivDist(
        name="Zeta_p",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(0.05, 0.4 * 0.05),
            lognorm2norm_std(0.05, 0.4 * 0.05),
        ],
        description="Primary damping ratio",
    ),
    UnivDist(
        name="Zeta_s",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(0.02, 0.5 * 0.02),
            lognorm2norm_std(0.02, 0.5 * 0.02),
        ],
        description="Secondary damping ratio",
    ),
    UnivDist(
        name="S0",
        distribution="lognormal",
        parameters=[
            lognorm2norm_mean(100.0, 0.1 * 100.0),
            lognorm2norm_std(100.0, 0.1 * 100.0),
        ],
        description="White noise base acceleration",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "DerKiureghian1991": {
        "name": "Damped-Oscillator-Der-Kiureghian-1991",
        "description": (
            "Probabilistic input model for the Damped Oscillator model "
            "from Der Kiureghian and De Stefano (1991)."
        ),
        "marginals": INPUT_MARGINALS_DERKIUREGHIAN1991,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "DerKiureghian1991"


class DampedOscillator(UQTestFunABC):
    """A concrete implementation of the Damped oscillator test function."""

    _TAGS = ["metamodeling", "sensitivity"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = 8

    _DESCRIPTION = (
        "Damped oscillator model from Igusa and Der Kiureghian (1985)"
    )

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        name: Optional[str] = None,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )
        # Process the default name
        if name is None:
            name = DampedOscillator.__name__

        super().__init__(prob_input=prob_input, name=name)

    def evaluate(self, xx: np.ndarray):
        """Evaluate the damped oscillator model on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            A 7-dimensional input values given by an N-by-7 array
            where N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the damped oscillator model test function, i.e.,
            the relative displacement of the secondary spring.
        """
        yy = evaluate_mean_square_displacement(xx)

        return np.sqrt(yy)


def evaluate_mean_square_displacement(xx: np.ndarray):
    """Evaluate the mean-square displacement of the damped oscillator model.

    Parameters
    ----------
    xx : np.ndarray
        A 7-dimensional input values given by an N-by-7 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The mean-square relative displacement of the secondary spring.
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

    # Compute the mean-square relative displacement of the secondary spring
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

    return xx_s
