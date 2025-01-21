"""
This module implements the cooling coffee cup model described in Tennøe (2018).

The cooling coffee cup model simulates the temperature evolution of a coffee
cup as it cools to an ambient temperature by solving an initial value problem
(using `solve_ivp()` from SciPy).
As a UQ test function, the model is expressed as a two-dimensional,
vector-valued function.

The model was featured in [1] and [2] as an introductory example
for metamodeling.

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

from uqtestfuns.core.custom_typing import (
    MarginalSpecs,
    FunParamSpecs,
    ProbInputSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["CoffeeCup"]


MARGINALS_TENNOEE2018: MarginalSpecs = [
    {
        "name": "kappa",
        "distribution": "uniform",
        "parameters": [0.025, 0.075],
        "description": "Thermal conductivity of the cup",
    },
    {
        "name": "temp_amb",
        "distribution": "uniform",
        "parameters": [15.0, 25.0],
        "description": "Ambient temperature [degC]",
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Tennoee2018": {
        "function_id": "CoffeeCup",
        "description": (
            "Probabilistic input model for the cooling coffee cup model "
            "from Tennøe et al. (2018)"
        ),
        "marginals": MARGINALS_TENNOEE2018,
        "copulas": None,
    },
}


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Tennoee2018": {
        "function_id": "CoffeeCup",
        "description": (
            "Parameter set for the cooling cup coffee cup model "
            "Tennøe et al. (2018)"
        ),
        "declared_parameters": [
            {
                "keyword": "temp_0",
                "value": 95.0,
                "type": float,
                "description": "Initial temperature [degC]",
            },
            {
                "keyword": "t_e",
                "value": 200.0,
                "type": float,
                "description": "End of transient [s]",
            },
            {
                "keyword": "n_ts",
                "value": 150,
                "type": int,
                "description": "Number of time steps",
            },
        ],
    },
}


def fun_ivp(t: float, temp: float, kappa: float, temp_amb: float) -> float:
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
    return float(-1 * kappa * (temp - temp_amb))


def evaluate(
    xx: np.ndarray, temp_0: float, t_e: float, n_ts: int, **kwargs
) -> np.ndarray:
    """Compute the temperature evolution of the cooling coffee cup.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.
    temp_0 : float
        The initial temperature of the coffee cup in degC.
    t_e : float
        The end of the transient in seconds.
    n_ts : int
        The number of time steps in the IVP solution.
    kwargs : dict
        The additional parameters as dictionary to be passed to `solve_ivp()`.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 2-dimensional array of shape (N, n_ts).
    """

    # Initialize the output
    yy = np.empty((len(xx), n_ts))

    # Get solve_ivp kwargs
    solve_ivp_kwargs = kwargs.get("solve_ivp", {})

    for i in range(len(xx)):

        # Get the realization of uncertain inputs
        kappa = xx[i, 0]
        temp_amb = xx[i, 1]

        # Solve the IVP
        sol = solve_ivp(
            fun_ivp,
            t_span=(0.0, t_e),
            y0=[temp_0],
            t_eval=np.linspace(0.0, t_e, n_ts),
            args=(kappa, temp_amb),
            **solve_ivp_kwargs,
        )

        yy[i, :] = sol.y[0]

    return yy


class CoffeeCup(UQTestFunFixDimABC):
    """Concrete implementation of the cooling coffee cup model."""

    _tags = ["metamodeling"]
    _description = "Cooling coffee cup model from Tennøe et al. (2018)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS

    evaluate = staticmethod(evaluate)  # type: ignore
