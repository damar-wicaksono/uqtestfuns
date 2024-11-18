"""
Module with an implementation of the flood model.

The flood model from [1] is an eight-dimensional scalar-valued function that
computes the maximum annual underflow of a river (in [m]).
A negative value indicates that an overflow (flooding) occurs.
The model is used in the context of sensitivity analysis in [1] and [2]
and has become a canonical example of the OpenTURNS package [3].

The model is based on a simplification of the one-dimensional hydro-dynamical
equations of St. Venant under the assumption of uniform and constant flow rate
and a large rectangular section.

References
----------
1. B. Iooss and P. Lemaître, “A Review on Global Sensitivity Analysis
   Methods,” in Uncertainty Management in Simulation-Optimization of
   Complex Systems, vol. 59, G. Dellino and C. Meloni, Eds.
   Boston, MA: Springer US, 2015, pp. 101–122.
   DOI: 10.1007/978-1-4899-7547-8_5
2. M. Lamboni, B. Iooss, A.-L. Popelin, and F. Gamboa, “Derivative-based
   global sensitivity measures: General links with Sobol’ indices
   and numerical tests,” Mathematics and Computers in Simulation, vol. 87,
   pp. 45–54, 2013.
   DOI: 10.1016/j.matcom.2013.02.002
3. M. Baudin, A. Dutfoy, B. Iooss, and A.-L. Popelin, “OpenTURNS:
   An Industrial Software for Uncertainty Quantification in Simulation,”
   in Handbook of Uncertainty Quantification, R. Ghanem, D. Higdon,
   and H. Owhadi, Eds. Cham: Springer International Publishing, 2017,
   pp. 2001–2038.
   DOI: 10.1007/978-3-319-12385-1_64
"""

import numpy as np

from uqtestfuns.core.custom_typing import MarginalSpecs, ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Flood"]


MARGINALS_IOOSS2015: MarginalSpecs = [  # From Ref. [1]
    {
        "name": "Q",
        "distribution": "trunc-gumbel",
        "parameters": [1013.0, 558.0, 500.0, 3000.0],
        "description": "Maximum annual flow rate [m^3/s]",
    },
    {
        "name": "Ks",
        "distribution": "trunc-normal",
        "parameters": [30.0, 8.0, 15.0, np.inf],
        "description": "Strickler coefficient [m^(1/3)/s]",
    },
    {
        "name": "Zv",
        "distribution": "triangular",
        "parameters": [49.0, 51.0, 50.0],
        "description": "River downstream level [m]",
    },
    {
        "name": "Zm",
        "distribution": "triangular",
        "parameters": [54.0, 56.0, 55.0],
        "description": "River upstream level [m]",
    },
    {
        "name": "Hd",
        "distribution": "uniform",
        "parameters": [7.0, 9.0],
        "description": "Dyke height [m]",
    },
    {
        "name": "Cb",
        "distribution": "triangular",
        "parameters": [55.0, 56.0, 55.5],
        "description": "Bank level [m]",
    },
    {
        "name": "L",
        "distribution": "triangular",
        "parameters": [4990.0, 5010.0, 5000.0],
        "description": "Length of the river stretch [m]",
    },
    {
        "name": "B",
        "distribution": "triangular",
        "parameters": [295.0, 305.0, 300.0],
        "description": "River width [m]",
    },
]

AVAILABLE_INPUTS: ProbInputSpecs = {
    "Iooss2015": {
        "function_id": "Flood",
        "description": (
            "Probabilistic input model for the Flood model "
            "from Iooss and Lemaître (2015)"
        ),
        "marginals": MARGINALS_IOOSS2015,
        "copulas": None,
    },
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the flood model test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A six-dimensional input values given by an N-by-8 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the flood model test function, i.e.,
        the height of a river.
        The output is a one-dimensional array of length N.
    """
    qq = xx[:, 0]  # Maximum annual flow rate
    kk_s = xx[:, 1]  # Strickler coefficient
    zz_v = xx[:, 2]  # River downstream level
    zz_m = xx[:, 3]  # River upstream level
    hh_d = xx[:, 4]  # Dyke height
    cc_b = xx[:, 5]  # Bank level
    ll = xx[:, 6]  # Length of the river stretch
    bb = xx[:, 7]  # River width

    # Compute the maximum annual height of the river [m]
    hh_w = (qq / (bb * kk_s * np.sqrt((zz_m - zz_v) / ll))) ** 0.6

    # Compute the maximum annual underflow [m]
    # NOTE: The sign compared to [1] has been inverted below, a negative
    # value indicates an overflow
    ss = cc_b + hh_d - zz_v - hh_w

    return ss


class Flood(UQTestFunFixDimABC):
    """Concrete implementation of the Flood model test function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Flood model from Iooss and Lemaître (2015)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = None

    evaluate = staticmethod(evaluate)  # type: ignore
