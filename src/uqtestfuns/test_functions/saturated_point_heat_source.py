"""
Module with an implementation of the saturated point heat source model.

The saturated point heat source model computes the thermo-hydro-mechanical
response of a saturated porous medium to a steady point heat source, yielding
three output fields: temperature change (delta T), pore-fluid pressure (p),
and radial displacement (u_r). The analytical solution is evaluated
on a user-specified grid of radial distances and times.
As a UQ test function, the model accepts eight uncertain material parameters
and returns a three-dimensional field output of shape (3, N_r, N_t).
It was used in [3] for global sensitivity analysis.

References
----------

1. J. R. Booker and C. Savvidou, "Consolidation around a Point Heat Source,"
   International Journal for Numerical and Analytical Methods in Geomechanics,
   vol. 9, no. 2, pp. 173–184, 1985. DOI: 10.1002/nag.1610090206
2. A. A. Chaudhry, J. Buchwald, O. Kolditz, and T. Nagel, "Consolidation around
   a Point Heat Source (Correction and Verification)," International Journal
   for Numerical and Analytical Methods in Geomechanics, vol. 43,
   pp. 2743–2751, 2019. DOI: 10.1002/nag.2998
3. A. A. Chaudhry, J. Buchwald, and T. Nagel, "Local and Global Spatio-temporal
   Sensitivity Analysis of Thermal Consolidation Around a Point Heat Source,"
   International Journal of Rock Mechanics and Mining Sciences, vol. 139,
   p. 104662, 2021. DOI: 10.1016/j.ijrmms.2021.104662
"""

import numpy as np

from scipy.special import erfc
from typing import List, Tuple, Union


def evaluate(
    xx: np.ndarray,
    Q: float,
    a_w: float,
    mu_w: float,
    rr: np.ndarray,
    tt: np.ndarray,
) -> np.ndarray:
    """Evaluate the saturated point heat source model.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 8)`` array of uncertain input values. Columns correspond
        to K, C, rho, E, a_s, k_s, nu, phi in that order.
    Q : float
        Point heat source power [W].
    a_w : float
        Volumetric thermal expansion coefficient of water [1/K].
    mu_w : float
        Dynamic viscosity of water [Pa s].
    rr : array-like of float
        Radius query points [m], shape ``(N_r,)``. Must be strictly positive.
    tt : array-like of float
        Time query points [s], shape ``(N_t,)``. Must be non-negative.

    Returns
    -------
    np.ndarray
        Output array of shape ``(N, 3, N_r, N_t)``. The three field
        components along axis 1 are, in order: temperature change
        delta T [K], excess pore pressure p [Pa], and radial
        displacement u_r [m].
    """

    # Create output array
    rr = np.asarray(rr, dtype=float)
    tt = np.asarray(tt, dtype=float)
    out = np.empty((len(xx), 3, len(rr), len(tt)))

    # Get the individual inputs
    K = xx[:, 0]  # Total thermal conductivity
    C = xx[:, 1]  # Total specific heat capacity
    rho = xx[:, 2]  # Total density
    E = xx[:, 3]  # Young's modulus
    a_s = xx[:, 4]  # Volumetric thermal expansion coefficient of solid
    k_s = xx[:, 5]  # Intrinsic permeability
    nu = xx[:, 6]  # Poisson's ratio
    phi = xx[:, 7]  # Porosity

    # Compute thermal diffusivity, Eq. 12, [2]
    kappa = K / (C * rho)

    # Common prefactor Q/(4πK), shaped for broadcasting over (N_r, N_t)
    q_4piK = (Q / (4 * np.pi * K))[:, None, None]  # (N, 1, 1)

    # erfc front function (kappa), Eq. (18) in [2]
    ff_kappa = _ff(rr, tt, kappa)

    # --- Temperature rise
    delta_T = q_4piK * ff_kappa / rr[None, :, None]  # Eq. 23, [2]

    # Compute the Lamé parameters
    ll = E * nu / ((1 + nu) * (1 - 2 * nu))
    GG = E / (2 * (1 + nu))
    # Constrained modulus
    mm = ll + 2 * GG

    # Compute coefficient of consolidation / hydraulic diffusivity
    cc = k_s / mu_w * mm  # Eq. 13, [2]

    # Volumetric thermal expansion of mixture
    aa_u = phi * a_w + (1 - phi) * a_s  # Eq. 6, [2]

    # Thermal stress coefficient
    bb = (ll + 2 * GG / 3) * a_s  # Eq. 11, [2]

    # Thermal pressurization coefficient and pore pressure amplitude
    XX = aa_u * mm - bb  # Eq. (14) in [2]
    denom = 1 - cc / kappa  # Warning: singular when c is very close to kappa
    P1 = XX / denom  # (N,)

    # erfc front function (c), Eq. (18) in [2]
    ff_c = _ff(rr, tt, cc)

    # --- Excess pore pressure (Eq. (24) in [2])
    pp = P1[:, None, None] * q_4piK * (ff_kappa - ff_c) / rr[None, :, None]

    # Displacement shape
    # Eq. (19) in [2] with kappa
    gg_kappa = _gg(rr, tt, kappa, ff_kappa)
    # Eq. (19) in [2] with c
    gg_c = _gg(rr, tt, cc, ff_c)
    # Eqs. (15), (16), and (20) in [2]
    g_field = (P1 + bb)[:, None, None] * gg_kappa - P1[:, None, None] * gg_c

    # --- Displacement (Eq. (25) in [2])
    u_r = q_4piK / mm[:, None, None] * g_field

    out[:, 0, :, :] = delta_T
    out[:, 1, :, :] = pp
    out[:, 2, :, :] = u_r

    return out


def _ff(rr: np.ndarray, tt: np.ndarray, AA: np.ndarray) -> np.ndarray:
    """Compute the erfc front function on the (r, t) grid.

    Evaluates Eq. (18) in [2] for all combinations of radius, time,
    and parameter values.

    Parameters
    ----------
    rr : np.ndarray
        Radius query points, shape ``(N_r,)``.
    tt : np.ndarray
        Time query points, shape ``(N_t,)``.
    AA : np.ndarray
        Diffusivity values (one per sample), shape ``(N,)``.

    Returns
    -------
    np.ndarray
        The front function with a shape of ``(N, N_r, N_t)`` for
        all parameter values (``N``), radius query points (``N_r``),
        and time query points (``N_t``).
    """
    At = AA[:, None] * tt[None, :]  # (N, N_t)
    denom = 2.0 * np.sqrt(At)[:, None, :]  # (N, 1, N_t)

    return erfc(rr[None, :, None] / denom)  # (N, N_r, N_t)


def _gg(
    rr: np.ndarray,
    tt: np.ndarray,
    AA: np.ndarray,
    ff_A: np.ndarray,
) -> np.ndarray:
    """Compute the displacement shape function on the (r, t) grid.

    Evaluates Eq. (19) in [2] for all combinations of radius, time,
    and parameter values.

    Parameters
    ----------
    rr : np.ndarray
        Radius query points, shape ``(N_r,)``.
    tt : np.ndarray
        Time query points, shape ``(N_t,)``.
    AA : np.ndarray
        Diffusivity values (one per sample), shape ``(N,)``.
    ff_A : np.ndarray
        Precomputed ``_ff(rr, tt, AA)``, shape ``(N, N_r, N_t)``.

    Returns
    -------
    np.ndarray
        The displacement shape function with a shape of ``(N, N_r, N_t)`` for
        all parameter values (``N``), radius query points (``N_r``),
        and time query points (``N_t``).
    """
    At = AA[:, None] * tt[None, :]  # (N, N_t)
    At_r2 = At[:, None, :] / rr[None, :, None] ** 2  # (N, N_r, N_t) = At/r²

    term1 = At_r2
    term2 = (0.5 - At_r2) * ff_A
    term3 = np.sqrt(At_r2 / np.pi) * np.exp(-1.0 / (4.0 * At_r2))

    return term1 + term2 - term3


def output_shape(
    rr: List[Union[float, int]],
    tt: List[Union[float, int]],
    **kwargs,
) -> Tuple[int, int, int]:
    """Return the output shape for a single sample point.

    Parameters
    ----------
    rr : list of float or int
        Radius query points [m].
    tt : list of float or int
        Time query points [s].
    **kwargs
        Absorbs unused parameter keywords.

    Returns
    -------
    Tuple[int, int, int]
        ``(3, N_r, N_t)`` where ``N_r = len(rr)`` and ``N_t = len(tt)``.
    """
    return 3, len(rr), len(tt)
