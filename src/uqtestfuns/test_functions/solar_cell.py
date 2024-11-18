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
from typing import Tuple

from uqtestfuns.core.custom_typing import (
    MarginalSpecs,
    FunParamSpecs,
    ProbInputSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["SolarCell"]


MARGINALS_CONSTANTINE2015: MarginalSpecs = [
    {
        "name": "Isc",
        "distribution": "uniform",
        "parameters": [0.05989, 0.23958],
        "description": "Short-circuit current [A]",
    },
    {
        "name": "log_Is",
        "distribution": "uniform",
        "parameters": [np.log(2.2e-11), np.log(2.2e-7)],
        "description": "(log) Diode reverse saturation current [A]",
    },
    {
        "name": "n",
        "distribution": "uniform",
        "parameters": [1.0, 2.0],
        "description": "Ideality factor [-]",
    },
    {
        "name": "Rs",
        "distribution": "uniform",
        "parameters": [0.16625, 0.66500],
        "description": "Series resistance [Ohm]",
    },
    {
        "name": "Rp",
        "distribution": "uniform",
        "parameters": [93.75, 375.00],
        "description": "Parallel (shunt) resistance [Ohm]",
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Constantine2015": {
        "function_id": "SolarCell",
        "description": (
            "Probabilistic input model for the single-diode solar cell model "
            "from Constantine et al. (2015)"
        ),
        "marginals": MARGINALS_CONSTANTINE2015,
        "copulas": None,
    },
}


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Constantine2015": {
        "function_id": "SolarCell",
        "description": (
            "Parameter set for the single-diode solar cell model from "
            "Constantine et al. (2015)"
        ),
        "declared_parameters": [
            {
                "keyword": "n_s",
                "value": 1,
                "type": int,
                "description": "# of cells connected in series [-]",
            },
            {
                "keyword": "v_th",
                "value": 0.02585,
                "type": float,
                "description": "Thermal voltage at 25degC [V]",
            },
        ],
    },
}


def obj_fun_root(
    i: float,
    v: float,
    x: np.ndarray,
    n_s: int,
    v_th: float,
) -> float:
    """Compute the equation to get the root.

    Parameters
    ----------
    i : float
        The current [A]
    v : float
        The voltage [V]
    x : np.ndarray
        The input variables of the solar cell model: I_SC, I_S, n, R_S, R_P.
    n_s : int
        The number of cells connected in series.
    v_th : float
        The thermal voltage value at 25degC [V]

    Returns
    -------
    float
        The root objective function for implicit current; the function returns
        0 if the current corresponds to the given voltage.
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
    **kwargs,
) -> float:
    """Compute the current of the solar cell given a voltage value.

    Parameters
    ----------
    v : float
        The voltage [V]
    x : np.ndarray
        The input variables of the solar cell model: I_SC, I_S, n, R_S, R_P.
    n_s : int
        The number of cells connected in series.
    v_th : float
        The thermal voltage value at 25degC [V]

    Returns
    -------
    float
        The current that corresponds to the given voltage.
    """
    i0 = np.array([0.0])
    # Find the corresponding current as the root
    sol = root(obj_fun_root, i0, args=(v, x, n_s, v_th), **kwargs)
    i = sol.x

    return i


def compute_power_max(
    xx: np.ndarray,
    n_s: int,
    v_th: float,
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the maximum power a solar cell given its design parameters.

    Parameters
    ----------
    xx : np.ndarray
        A five-dimensional input values of the solar cell model given by
        an N-by-5 array where N is the number of input values.
    n_s : int
        The number of cells connected in series.
    v_th : float
        The thermal voltage value at 25degC [V]
    kwargs : dict
        The additional parameters to be passed either to `root()` or
        `minimize()`. A dictionary value of key `root` will be passed to
        `root()`, while a dictionary value of key `minimize` will be passed to
        `minimize()`

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        A pair of arrays containing the maximum power a solar cell and the
        corresponding voltage.
    """
    # Initialize output array
    pp_max = np.empty(len(xx))
    vv_max = np.empty(len(xx))

    # Get additional arguments for root and minimize
    root_kwargs = kwargs.get("root", {})
    minimize_kwargs = kwargs.get("minimize", {})

    for idx in range(len(xx)):
        # Set up the objective function (negated for minimization)
        x = xx[idx]

        def _obj_fun(v, x, n_s, v_th, root_kwargs):
            return -1 * v * compute_current(v, x, n_s, v_th, **root_kwargs)

        # Minimize the objective function
        v0 = np.array([0.0])
        res = minimize(
            _obj_fun,
            v0,
            args=(x, n_s, v_th, root_kwargs),
            **minimize_kwargs,
        )

        pp_max[idx] = -1 * res.fun  # Negated back for the maximum value
        vv_max[idx] = res.x

    return pp_max, vv_max


def evaluate(xx: np.ndarray, n_s: int, v_th: float, **kwargs) -> np.ndarray:
    """Evaluate the solar cell model on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A five-dimensional input values given by an N-by-5 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy, _ = compute_power_max(xx, n_s, v_th, **kwargs)

    return yy


class SolarCell(UQTestFunFixDimABC):
    """Concrete implementation of the single-diode solar cell model."""

    _tags = ["metamodeling", "sensitivity"]
    _description = (
        "Single-diode solar-cell model from Constantine et al. (2015)"
    )
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS

    evaluate = staticmethod(evaluate)  # type: ignore
