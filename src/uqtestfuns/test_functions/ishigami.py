"""
Module with an implementation of the Ishigami function.

The Ishigami test function is a three-dimensional scalar-valued function.
The function was first introduced in [1] in the context of sensitivity
analysis, and has been revisited many times in the same context
(see, for instances, [2], [3], [4]).

References
----------

1. T. Ishigami and T. Homma, “An importance quantification technique in
   uncertainty analysis for computer models,” in [1990] Proceedings.
   First International Symposium on Uncertainty Modeling and Analysis,
   College Park, MD, USA, 1991, pp. 398–403.
   DOI: 10.1109/ISUMA.1990.151285.
2. I. M. Sobol’ and Y. L. Levitan, “On the use of variance reducing multipliers
   in Monte Carlo computations of a global sensitivity index,”
   Computer Physics Communications, vol. 117, no. 1, pp. 52–61, 1999.
   DOI: 10.1016/S0010-4655(98)00156-8
3. B. Sudret, “Global sensitivity analysis using polynomial chaos expansions,”
   Reliability Engineering & System Safety, vol. 93, no. 7, pp. 964–979, 2008.
   DOI: 10.1016/j.ress.2007.04.002.
4. A. Marrel, B. Iooss, B. Laurent, and O. Roustant, "Calculations of
   Sobol indices for the Gaussian process metamodel,”
   Reliability Engineering & System Safety,
   vol. 94, no. 3, pp. 742–751, 2009.
   DOI:10.1016/j.ress.2008.07.008
"""

import numpy as np

from uqtestfuns.core.custom_typing import (
    MarginalSpecs,
    ProbInputSpecs,
    FunParamSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Ishigami"]


MARGINALS_ISHIGAMI1991: MarginalSpecs = [
    {
        "name": "X1",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": None,
    },
    {
        "name": "X2",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": None,
    },
    {
        "name": "X3",
        "distribution": "uniform",
        "parameters": [-np.pi, np.pi],
        "description": None,
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Ishigami1991": {
        "function_id": "Ishigami",
        "description": (
            "Probabilistic input model for the Ishigami function "
            "from Ishigami and Homma (1991)."
        ),
        "marginals": MARGINALS_ISHIGAMI1991,
        "copulas": None,
    },
}

AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Ishigami1991": {
        "function_id": "Ishigami",
        "description": (
            "Parameter set for the Ishigami function from Ishigami and Homma "
            "(1991)"
        ),
        "declared_parameters": [
            {
                "keyword": "a",
                "value": 7.0,
                "type": float,
                "description": None,
            },
            {
                "keyword": "b",
                "value": 0.1,
                "type": float,
                "description": None,
            },
        ],
    },
    "Sobol1999": {
        "function_id": "Ishigami",
        "description": (
            "Parameter set for the Ishigami function from Sobol' and Levitan "
            "(1999)"
        ),
        "declared_parameters": [
            {
                "keyword": "a",
                "value": 7.0,
                "type": float,
                "description": None,
            },
            {
                "keyword": "b",
                "value": 0.05,
                "type": float,
                "description": None,
            },
        ],
    },
}

DEFAULT_PARAMETERS_SELECTION = "Ishigami1991"


def evaluate(xx: np.ndarray, a: float, b: float) -> np.ndarray:
    """Evaluate the Ishigami function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        3-Dimensional input values given by N-by-3 arrays where
        N is the number of input values.
    a : float
        The first parameter of the Ishigami function.
    b : float
        The second parameter of the Ishigami function.

    Returns
    -------
    np.ndarray
        The output of the Ishigami function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    # Compute the Ishigami function
    term_1 = np.sin(xx[:, 0])
    term_2 = a * np.sin(xx[:, 1]) ** 2
    term_3 = b * xx[:, 2] ** 4 * np.sin(xx[:, 0])

    yy = term_1 + term_2 + term_3

    return yy


class Ishigami(UQTestFunFixDimABC):
    """An implementation of the Ishigami test function."""

    _tags = ["sensitivity"]
    _description = "Ishigami function from Ishigami and Homma (1991)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = DEFAULT_PARAMETERS_SELECTION

    evaluate = staticmethod(evaluate)  # type: ignore
