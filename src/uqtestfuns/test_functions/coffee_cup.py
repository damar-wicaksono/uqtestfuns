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
    t_end: float,
    n_ts: int,
    solve_ivp_kwargs: Optional[Dict[str, Any]],
) -> np.ndarray:
    """Compute the temperature evolution of the cooling coffee cup.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 2)`` array of input values.
    temp_0 : float
        The initial temperature of the coffee cup [degC].
    t_end : float
        The final time step [s]
    n_ts : int
        The number of time steps [-]
    solve_ivp_kwargs : dict, optional
        Additional keyword arguments passed to ``solve_ivp()``.
        If ``None``, default solver settings are used.

    Returns
    -------
    np.ndarray
        Temperature evolution at each of the ``n_ts`` time points.
        Shape is ``(N, n_ts)`` when ``n_ts > 1``, or ``(N,)`` when
        ``n_ts == 1``.
    """

    # Initialize the output
    yy = np.empty((len(xx), n_ts))

    # Time query points
    t_eval = np.linspace(0.0, t_end, n_ts)

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
            t_span=(0.0, t_end),
            y0=[temp_0],
            t_eval=t_eval,
            args=(kappa, temp_amb),
            **solve_ivp_kwargs,
        )

        yy[i, :] = sol.y[0]

    return yy[:, 0] if n_ts == 1 else yy


def output_shape(n_ts: int, **kwargs):
    """Return the output shape of the model for each sample point.

    Parameters
    ----------
    n_ts : int
        The number of time steps [-]

    Returns
    -------
    tuple
        The output shape of the model for each sample point.
    """
    return (n_ts,)
