"""
This module implements the solar cell model from Constantine et al. (2015).

The test function is a five-dimensional, scalar-valued function that models
the maximum power of a single-diode solar cell. The function was used in
Constantine et al. (2015) to demonstrate the active subspace method for
input dimension reduction and sensitivity analysis.

References
----------

1. P. G. Constantine, B. Zaharatos, and M. Campanelli, “Discovering an active
   subspace in a single‐diode solar cell model,” Statistical Analysis, vol. 8,
   no. 5–6, pp. 264–273, 2015.
   DOI: 10.1002/sam.11281
"""

import numpy as np

from scipy.optimize import root, minimize
from typing import Any, Dict, Optional, Tuple


def obj_fun_root(
    i: float,
    v: float,
    x: np.ndarray,
    n_s: int,
    v_th: float,
) -> float:
    """Compute the implicit current equation for root finding.

    Parameters
    ----------
    i : float
        The current [A].
    v : float
        The voltage [V].
    x : np.ndarray
        Input variables: Isc, log_Is, n, Rs, Rp.
    n_s : int
        Number of cells connected in series.
    v_th : float
        Thermal voltage at 25 degrees C [V].

    Returns
    -------
    float
        Residual of the implicit current equation; zero at the solution.
    """
    # Get the input variable values
    i_sc = x[0]
    i_s = np.exp(x[1])
    n = x[2]
    r_s = x[3]
    r_p = x[4]

    # Compute the photo current
    exp_term_1 = np.exp(i_sc * r_s / n_s / n / v_th) - 1
    i_l = i_sc + i_s * exp_term_1 + i_sc * r_s / r_p

    # Compute the objective function
    exp_term_2 = np.exp((v + i * r_s) / n_s / n / v_th) - 1
    y = i - i_l + i_s * exp_term_2 + (v + i * r_s) / r_p

    return y


def compute_current(
    v: float,
    x: np.ndarray,
    n_s: int,
    v_th: float,
    root_kwargs: Dict[str, Any],
) -> float:
    """Compute the current of the solar cell at a given voltage.

    Parameters
    ----------
    v : float
        The voltage [V].
    x : np.ndarray
        Input variables: Isc, log_Is, n, Rs, Rp.
    n_s : int
        Number of cells connected in series.
    v_th : float
        Thermal voltage at 25 degrees C [V].
    root_kwargs : dict, optional
        Keyword arguments passed to ``scipy.optimize.root``.

    Returns
    -------
    float
        The current corresponding to the given voltage [A].
    """
    i0 = np.array([0.0])
    # Find the corresponding current as the root
    sol = root(obj_fun_root, i0, args=(v, x, n_s, v_th), **root_kwargs)
    i = sol.x

    return i


def compute_power_max(
    xx: np.ndarray,
    n_s: int,
    v_th: float,
    root_kwargs: Dict[str, Any],
    minimize_kwargs: Dict[str, Any],
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the maximum power of the solar cell for each input sample.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 5)`` array of input values.
    n_s : int
        Number of cells connected in series.
    v_th : float
        Thermal voltage at 25 degrees C [V].
    root_kwargs : dict
        Keyword arguments passed to ``scipy.optimize.root``.
    minimize_kwargs : dict
        Keyword arguments passed to ``scipy.optimize.minimize``.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Arrays of maximum power and corresponding voltage for each sample.
    """
    # Initialize output array
    pp_max = np.empty(len(xx))
    vv_max = np.empty(len(xx))

    for idx in range(len(xx)):
        # Set up the objective function (negated for minimization)
        x = xx[idx]

        def _obj_fun(v, x_, n_s_, v_th_, root_kwargs_):
            return -1 * v * compute_current(v, x_, n_s_, v_th_, root_kwargs_)

        # Minimize the objective function
        v0 = np.array([0.0])
        res = minimize(
            _obj_fun,
            v0,
            args=(x, n_s, v_th, root_kwargs),
            **minimize_kwargs,
        )

        pp_max[idx] = -1 * res.fun  # Negated back for the maximum value
        vv_max[idx] = res.x[0]

    return pp_max, vv_max


def evaluate(
    xx: np.ndarray,
    n_s: int,
    v_th: float,
    root_kwargs: Optional[Dict[str, Any]] = None,
    minimize_kwargs: Optional[Dict[str, Any]] = None,
) -> np.ndarray:
    """Evaluate the solar cell model on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 5)`` array of input values where ``N`` is the number of
        evaluation points.
    n_s : int
        Number of cells connected in series.
    v_th : float
        Thermal voltage at 25 degrees C [V].
    root_kwargs : dict, optional
        Keyword arguments passed to ``scipy.optimize.root``.
        ``None`` uses default solver settings.
    minimize_kwargs : dict, optional
        Keyword arguments passed to ``scipy.optimize.minimize``.
        ``None`` uses default solver settings.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N`` containing the maximum
        power of the solar cell for each input sample [W].
    """
    # Get the root and minimize kwargs
    root_ = root_kwargs or {}
    minimize_ = minimize_kwargs or {}

    yy, _ = compute_power_max(xx, n_s, v_th, root_, minimize_)

    return yy
