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

from scipy.special import erfc, erf
from typing import List, Tuple, Union

_SQRT_PI = np.sqrt(np.pi)
_RATIO_TOL = 1e-4  # switch to Taylor when |delta| * max(1, z^2) < this


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
        Radius query points [m], 1-D, all entries strictly positive.
    tt : array-like of float
        Time query points [s], 1-D, all entries non-negative (zero allowed).

    Returns
    -------
    np.ndarray
        Output array of shape ``(N, 3, N_r, N_t)``. The three field
        components along axis 1 are, in order: temperature change
        delta T [K], excess pore pressure p [Pa], and radial
        displacement u_r [m].
    """

    rr = np.asarray(rr, dtype=float)
    tt = np.asarray(tt, dtype=float)

    if rr.ndim != 1:
        raise ValueError(f"rr must be 1-dimensional, got shape {rr.shape}.")
    if tt.ndim != 1:
        raise ValueError(f"tt must be 1-dimensional, got shape {tt.shape}.")
    if not np.all(rr > 0):
        raise ValueError(
            "All entries of rr must be strictly positive (rr > 0)."
        )
    if not np.all(tt >= 0):
        raise ValueError("All entries of tt must be non-negative (tt >= 0).")

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

    # Thermal pressurization coefficient, Eq. (14) in [2]
    XX = aa_u * mm - bb  # (N,)

    # erfc front function (c), Eq. (18) in [2]
    ff_c = _ff(rr, tt, cc)

    # --- Excess pore pressure (Eq. (24) in [2])
    rr_f = _ratio_f(rr, tt, kappa, cc, ff_kappa, ff_c)
    pp = XX[:, None, None] * q_4piK / rr[None, :, None] * rr_f

    # Displacement shape
    gg_kappa = _gg(rr, tt, kappa, ff_kappa)  # Eq. (19) in [2] with kappa
    gg_c = _gg(rr, tt, cc, ff_c)  # Eq. (19) in [2] with c
    rr_g = _ratio_g(rr, tt, kappa, cc, gg_kappa, gg_c)
    # Eqs. (15), (16), and (20) in [2]
    g_field = bb[:, None, None] * gg_kappa + XX[:, None, None] * rr_g

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

    # At t = 0, the denominator is 0, giving r/0 = inf;
    # but erfc(inf) = 0 is well-defined: Suppress the warning.
    with np.errstate(divide="ignore", invalid="ignore"):
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


def _ratio_f(
    rr: np.ndarray,
    tt: np.ndarray,
    kappa: np.ndarray,
    cc: np.ndarray,
    ff_kappa: np.ndarray,
    ff_c: np.ndarray,
) -> np.ndarray:
    """Compute R_f = (f^kappa - f^c) / (1 - c/kappa), stable near c = kappa.

    Uses a quadratic Taylor expansion in delta = 1 - c/kappa when
    |delta| * max(1, z^2) < _RATIO_TOL, the direct quotient otherwise.
    Series derived symbolically; verified against 60-digit reference.

    z = r / (2 sqrt(kappa t)).

    Parameters
    ----------
    rr : np.ndarray
        Radius query points, shape ``(N_r,)``.
    tt : np.ndarray
        Time query points, shape ``(N_t,)``.
    kappa : np.ndarray
        Thermal diffusivity values, shape ``(N,)``.
    cc : np.ndarray
        Hydraulic diffusivity values, shape ``(N,)``.
    ff_kappa : np.ndarray
        Precomputed ``_ff(rr, tt, kappa)``, shape ``(N, N_r, N_t)``.
    ff_c : np.ndarray
        Precomputed ``_ff(rr, tt, cc)``, shape ``(N, N_r, N_t)``.

    Returns
    -------
    np.ndarray
        Shape ``(N, N_r, N_t)``.
    """
    # delta = 1 - c/kappa: zero at the singularity, negative when c > kappa
    delta = (1.0 - cc / kappa)[:, None, None]  # (N, 1, 1)

    # z = r / (2 sqrt(kappa t)): erfc argument at thermal diffusivity.
    # errstate: at t=0, sqrt(0)=0 so z=inf; erfc(inf)=0, the result is correct.
    At = kappa[:, None] * tt[None, :]  # (N, N_t)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = rr[None, :, None] / (2.0 * np.sqrt(At)[:, None, :])  # (N,N_r,N_t)

    # Broadcast delta to (N, N_r, N_t) for element-wise masking with z.
    delta_bc = np.broadcast_to(delta, z.shape)

    # Switch to Taylor where the direct quotient loses precision.
    # The erfc argument for c differs from z by ~|delta|/2, so the two erfc
    # values agree to ~|delta| relative digits; for large z they agree to
    # ~|delta|*z^2 because erfc decays fast there. Hence, the z^2 scaling.
    near = np.abs(delta_bc) * np.maximum(1.0, z**2) < _RATIO_TOL

    out = np.empty_like(ff_kappa)
    # Direct quotient: safe wherever near is False.
    # errstate: delta=0 gives 0/0=NaN, but near=True there, so it is unused.
    with np.errstate(divide="ignore", invalid="ignore"):
        out[~near] = ((ff_kappa - ff_c) / delta)[~near]

    # Taylor branch: extract the near-singular elements as 1-D arrays to
    # avoid evaluating exp(-z^2) at z=inf (t=0 entries, where near=False).
    zn, dn = z[near], delta_bc[near]
    z2n = zn**2

    # Quadratic Taylor expansion of R_f in delta, via L'Hopital at delta=0:
    #   R_f ~ (z e^{-z^2} / sqrt(pi)) * (1 + c1*delta + c2*delta^2)
    # Coefficients from expanding z_c = z/sqrt(1-delta) and differentiating:
    #   c1 = 3/4 - z^2/2
    #   c2 = 5/8 - 5*z^2/6 + z^4/6
    c1 = 3 / 4 - z2n / 2
    c2 = 5 / 8 - 5 / 6 * z2n + z2n**2 / 6
    out[near] = zn * np.exp(-z2n) / _SQRT_PI * (1.0 + c1 * dn + c2 * dn**2)

    return out


def _ratio_g(
    rr: np.ndarray,
    tt: np.ndarray,
    kappa: np.ndarray,
    cc: np.ndarray,
    gg_kappa: np.ndarray,
    gg_c: np.ndarray,
) -> np.ndarray:
    """Compute R_g = (g^kappa - g^c) / (1 - c/kappa), stable near c = kappa.

    Uses a quadratic Taylor expansion in delta = 1 - c/kappa when
    |delta| * max(1, z^2) < _RATIO_TOL, the direct quotient otherwise.
    Series derived symbolically; verified against 60-digit reference.

    Parameters
    ----------
    rr : np.ndarray
        Radius query points, shape ``(N_r,)``.
    tt : np.ndarray
        Time query points, shape ``(N_t,)``.
    kappa : np.ndarray
        Thermal diffusivity values, shape ``(N,)``.
    cc : np.ndarray
        Hydraulic diffusivity values, shape ``(N,)``.
    gg_kappa : np.ndarray
        Precomputed ``_gg(rr, tt, kappa, ff_kappa)``, shape ``(N, N_r, N_t)``.
    gg_c : np.ndarray
        Precomputed ``_gg(rr, tt, cc, ff_c)``, shape ``(N, N_r, N_t)``.

    Returns
    -------
    np.ndarray
        Shape ``(N, N_r, N_t)``.
    """
    # Same setup as _ratio_f: delta, z, near mask.
    delta = (1.0 - cc / kappa)[:, None, None]  # (N, 1, 1)
    At = kappa[:, None] * tt[None, :]  # (N, N_t)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = rr[None, :, None] / (2.0 * np.sqrt(At)[:, None, :])  # (N,N_r,N_t)
    delta_bc = np.broadcast_to(delta, z.shape)
    near = np.abs(delta_bc) * np.maximum(1.0, z**2) < _RATIO_TOL

    out = np.empty_like(gg_kappa)
    with np.errstate(divide="ignore", invalid="ignore"):
        out[~near] = ((gg_kappa - gg_c) / delta)[~near]

    zn, dn = z[near], delta_bc[near]
    z2n = zn**2

    # Quadratic Taylor expansion of R_g in delta.
    # G(z) denotes g^A written in z = r/(2 sqrt(At)).  The expansion is:
    #   R_g ~ -G'(z)*z/2 + (-3G'(z)*z/8 - G''(z)*z^2/8)*delta + ...
    #
    # Zeroth-order term (delta=0 limit): -G'(z)*z/2.
    # G'(z) = -erf(z)/(2z^3) + exp(-z^2)/(sqrt(pi)*z^2), so:
    #   -G'(z)*z/2 = (erf(z) - 2z exp(-z^2)/sqrt(pi)) / (4z^2)
    limit = (erf(zn) - 2.0 / _SQRT_PI * zn * np.exp(-z2n)) / (4.0 * z2n)

    # Linear and quadratic corrections: the 3G' and G'' terms simplify to
    #   c1 = 1/4, c2 = 5/24 - z^2/12  (both multiplied by z exp(-z^2)/sqrt(pi))
    corr = (
        zn * np.exp(-z2n) / _SQRT_PI * (dn / 4 + (5 / 24 - z2n / 12) * dn**2)
    )

    out[near] = limit + corr

    return out


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
