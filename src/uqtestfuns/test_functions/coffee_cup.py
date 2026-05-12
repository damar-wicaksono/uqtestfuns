"""
Module with an implementation of the cooling coffee cup model.

The cooling coffee cup model simulates the temperature evolution of a coffee
cup as it cools to an ambient temperature by solving an initial value problem
using `solve_ivp()` from SciPy. As a UQ test function, the model is expressed
as a two-dimensional, vector-valued function introduced in [1]
as an introductory example for metamodeling (see also [2]).

References
----------

1. S. Tennøe, G. Halnes, and G. T. Einevoll, “Uncertainpy: A Python Toolbox
   for Uncertainty Quantification and Sensitivity Analysis
   in Computational Neuroscience,” Frontier in Neuroinformatics, vol. 12,
   p. 49, 2018.
   DOI: 10.3389/fninf.2018.00049
2. R. A. Richardson, D. W. Wright, W. Edeling, V. Jancauskas, J. Lakhlili,
   and P. V. Coveney, “EasyVVUQ: A Library for Verification, Validation
   and Uncertainty Quantification in High Performance Computing,”
   Journal of Open Research Software, vol. 8, no. 1, p. 11, 2020.
   DOI: 10.5334/jors.303
"""

import numpy as np

from scipy.integrate import solve_ivp
from typing import Any, Dict, Optional

# --- Time grid parameters: fixed to ensure unambiguous output dimension
# end of transient [s]
_T_END = 200.0
# number of time steps
_N_TS = 150
# evaluation time points
_T_EVAL = np.linspace(0.0, _T_END, _N_TS)


def fun_ivp(t: float, temp: float, kappa: float, temp_amb: float):
    """The right-hand side of the initial value problem.

    Parameters
    ----------
    t : float
        The current time.
    temp :float
        The current temperature.
    kappa : float
        Thermal conductivity of the cup.
    temp_amb : float
        Ambient temperature.
    """
    return -1 * kappa * (temp - temp_amb)


def evaluate(
    xx: np.ndarray,
    temp_0: float,
    solve_ivp_kwargs: Optional[Dict[str, Any]],
) -> np.ndarray:
    """Compute the temperature evolution of the cooling coffee cup.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 2)`` array of input values.
    temp_0 : float
        The initial temperature of the coffee cup [degC].
    solve_ivp_kwargs : dict, optional
        Additional keyword arguments passed to ``solve_ivp()``.
        If ``None``, default solver settings are used.

    Returns
    -------
    np.ndarray
        A two-dimensional array of shape ``(N, 150)`` containing the
        temperature evolution at 150 evenly spaced time points over
        200 seconds.
    """

    # Initialize the output
    yy = np.empty((len(xx), _N_TS))

    # Get solve_ivp kwargs
    if solve_ivp_kwargs is None:
        solve_ivp_kwargs = {}

    for i in range(len(xx)):

        # Get the realization of uncertain inputs
        kappa = xx[i, 0]
        temp_amb = xx[i, 1]

        # Solve the IVP
        sol = solve_ivp(
            fun_ivp,
            t_span=(0.0, _T_END),
            y0=[temp_0],
            t_eval=_T_EVAL,
            args=(kappa, temp_amb),
            **solve_ivp_kwargs,
        )

        yy[i, :] = sol.y[0]

    return yy
