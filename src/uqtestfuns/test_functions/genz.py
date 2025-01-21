"""
Module with implementations of integral test functions from Genz (1984).

Genz [1] introduced six challenging parameterized $M$-dimensional functions
designed to test the performance of numerical integration routines:

- Oscillatory function features an oscillating shape in the multidimensional
  space.
- Product peak function features a prominent peak at the center
  of the multidimensional space.
- Corner peak function features a prominent peak in one corner
  of the multidimensional space. This function was featured as a test function
  in sensitivity analysis ([2]) and metamodeling ([3]) exercises.
- Gaussian function features a bell-shaped peak at the center
  of the multidimensional space.
- Continuous function features an exponential decay from the center
  of the multidimensional space. The function is continuous everywhere,
  but non-differentiable at the center.
- Discontinuous function features an exponential rise from corner
  of the multidimensional space up to the offset parameter value,
  after which the function value drops to zero everywhere,
  creating discontinuity. This function was featured as a test function
  in sensitivity analysis ([2])

The functions are further characterized by shift and scale parameters.
While the shift parameter has minimal impact on the integral's value,
the scale parameter significantly affects
the difficulty of the integration problem.

References
----------

1. A. Genz, “Testing Multidimensional Integration Routines,”
   in Proc. of International Conference on Tools, Methods and Languages
   for Scientific and Engineering Computation, USA: Elsevier North-Holland,
   Inc., 1984, pp. 81–94.
2. X. Zhang and M. D. Pandey, “An effective approximation for variance-based
   global sensitivity analysis,” Reliability Engineering & System Safety,
   vol. 121, pp. 164–174, 2014.
   DOI: 10.1016/j.ress.2013.07.010
3. J. D. Jakeman, M. S. Eldred, and K. Sargsyan, “Enhancing l1-minimization
   estimates of polynomial chaos expansions using basis selection,”
   Journal of Computational Physics, vol. 289, pp. 18–34, 2015.
   DOI: 10.1016/j.jcp.2015.02.025.
"""

import numpy as np

from uqtestfuns.core.custom_typing import (
    FunParamSpecs,
    MarginalSpecs,
    ProbInputSpecs,
)
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = [
    "GenzContinuous",
    "GenzCornerPeak",
    "GenzDiscontinuous",
    "GenzGaussian",
    "GenzOscillatory",
    "GenzProductPeak",
]


MARGINALS_GENZ1984: MarginalSpecs = [
    {
        "name": "X",
        "distribution": "uniform",
        "parameters": [0.0, 1.0],
        "description": None,
    }
]


def _get_aa_genz_1984(input_dimension: int) -> np.ndarray:
    """Construct an array of shape parameters for the Genz functions [1]."""
    aa = 5.0 * np.ones(input_dimension)

    return aa


def _get_bb_genz_1984(input_dimension: int) -> np.ndarray:
    """Construct an array of shape parameters for the Genz functions [1]."""
    bb = 0.5 * np.ones(input_dimension)

    return bb


def _get_aa_zhang_2014_1(input_dimension: int) -> np.ndarray:
    """Construct a scaling array for the Genz function from [2] (3D case).

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    - The test function was originally limited to three dimensions; here,
      the values beyond dimension 3 are extrapolated.
    """
    aa = 0.02 + 0.03 * np.arange(input_dimension)

    return aa


def _get_aa_zhang_2014_2(input_dimension: int) -> np.ndarray:
    """Construct a scaling array for the Genz function from [2] (10D case).

    Notes
    -----
    - The parameters were defined only for the corner peak function.
    - The test function was originally limited to ten dimensions; here,
      the values beyond dimension 10 are extrapolated.
    """
    aa = 0.1 * np.arange(1, input_dimension + 1)

    return aa


def evaluate_oscillatory(
    xx: np.ndarray, aa: np.ndarray, b: float
) -> np.ndarray:
    """Evaluate the oscillatory function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.
    b : float
        The scalar shift parameter of the Genz family of integrand.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.cos(2 * np.pi * b + np.sum(xx * aa, axis=1))

    return yy


class GenzOscillatory(UQTestFunVarDimABC):
    """A concrete implementation of the Genz oscillatory function."""

    _tags = ["integration"]
    _description = "Oscillatory integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzOscillatory",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzOscillatory",
            "description": (
                "Parameter set for the oscillatory function from Genz (1984);"
                " constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
                {
                    "keyword": "b",
                    "value": 0.5,
                    "type": float,
                    "description": "Offset parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_oscillatory)  # type: ignore


def evaluate_corner_peak(xx: np.ndarray, aa: np.ndarray) -> np.ndarray:
    """Evaluate the corner peak function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    dim = xx.shape[1]

    yy = (1 + (xx @ aa)) ** (-(dim + 1))

    return yy


class GenzCornerPeak(UQTestFunVarDimABC):
    """A concrete implementation of the corner peak from Genz (1984)."""

    _tags = ["integration", "metamodeling", "sensitivity"]
    _description = "Corner peak integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Genz (1984); "
                "constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
            ],
        },
        "Zhang2014-1": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Zhang and "
                "Pandey (2014); Section 4.4 (3D case), linearly increasing"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_zhang_2014_1,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
            ],
        },
        "Zhang2014-2": {
            "function_id": "GenzCornerPeak",
            "description": (
                "Parameter set for the corner peak function from Zhang and "
                "Pandey (2014); Section 4.4 (10D case), linearly increasing"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_zhang_2014_2,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_corner_peak)  # type: ignore


def evaluate_product_peak(
    xx: np.ndarray, aa: np.ndarray, bb: np.ndarray
) -> np.ndarray:
    """Compute the product peak function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.
        The length of the vector must M.
    bb : np.ndarray
        The vector of offset parameters of the Genz family of integrand
        functions; the values do not alter significantly the difficulty of
        the integration problem.
        The length of the vector must be M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.prod(1 / ((xx - bb) ** 2 + aa ** (-2)), axis=1)

    return yy


class GenzProductPeak(UQTestFunVarDimABC):
    """A concrete implementation of the product peak from Genz (1984)."""

    _tags = ["integration"]
    _description = "Product peak integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzProductPeak",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzProductPeak",
            "description": (
                "Parameter set for the product peak function from Genz (1984);"
                " constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
                {
                    "keyword": "bb",
                    "value": _get_bb_genz_1984,
                    "type": np.ndarray,
                    "description": "Offset parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_product_peak)  # type: ignore


def evaluate_gaussian(
    xx: np.ndarray, aa: np.ndarray, bb: np.ndarray
) -> np.ndarray:
    """Compute the Gaussian function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.
        The length of the vector must M.
    bb : np.ndarray
        The vector of offset parameters of the Genz family of integrand
        functions; the values do not alter significantly the difficulty of
        the integration problem.
        The length of the vector must be M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(-1 * np.sum((xx - bb) ** 2 * aa**2, axis=1))

    return yy


class GenzGaussian(UQTestFunVarDimABC):
    """A concrete implementation of the Genz Gaussian function."""

    _tags = ["integration"]
    _description = "Gaussian integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzGaussian",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzGaussian",
            "description": (
                "Parameter set for the continuous function from Genz (1984);"
                " constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
                {
                    "keyword": "bb",
                    "value": _get_bb_genz_1984,
                    "type": np.ndarray,
                    "description": "Offset parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_gaussian)  # type: ignore


def evaluate_continuous(
    xx: np.ndarray, aa: np.ndarray, bb: np.ndarray
) -> np.ndarray:
    """Compute the continuous function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.
        The length of the vector must M.
    bb : np.ndarray
        The vector of offset parameters of the Genz family of integrand
        functions; the values do not alter significantly the difficulty of
        the integration problem.
        The length of the vector must be M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(-1 * np.sum(np.abs(xx - bb) * aa, axis=1))

    return yy


class GenzContinuous(UQTestFunVarDimABC):
    """A concrete implementation of the Genz continuous function."""

    _tags = ["integration"]
    _description = (
        "Continuous (but non-differentiable) integrand from Genz (1984)"
    )
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzContinuous",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzContinuous",
            "description": (
                "Parameter set for the continuous function from Genz (1984);"
                " constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
                {
                    "keyword": "bb",
                    "value": _get_bb_genz_1984,
                    "type": np.ndarray,
                    "description": "Offset parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_continuous)  # type: ignore


def evaluate_discontinuous(
    xx: np.ndarray, aa: np.ndarray, bb: np.ndarray
) -> np.ndarray:
    """Compute the discontinuous function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of shape parameters of the Genz family of integrand
        functions; the larger the value the more difficult the integrations.
        The length of the vector must M.
    bb : np.ndarray
        The vector of offset parameters of the Genz family of integrand
        functions; the values do not alter significantly the difficulty of
        the integration problem.
        The length of the vector must be M.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(np.sum(xx * aa, axis=1))

    # Filter the output to make the function discontinuous
    mask = np.zeros(xx.shape[0], dtype=bool)
    for i in range(xx.shape[1]):
        mask |= xx[:, i] > bb[i]
    yy[mask] = 0

    return yy


class GenzDiscontinuous(UQTestFunVarDimABC):
    """A concrete implementation of the Genz discontinuous function."""

    _tags = ["integration", "sensitivity"]
    _description = "Discontinuous integrand from Genz (1984)"
    _available_inputs: ProbInputSpecs = {
        "Genz1984": {
            "function_id": "GenzDiscontinuous",
            "description": (
                "Input specification for the Genz family of integrand"
            ),
            "marginals": MARGINALS_GENZ1984,
            "copulas": None,
        }
    }
    _available_parameters: FunParamSpecs = {
        "Genz1984": {
            "function_id": "GenzDiscontinuous",
            "description": (
                "Parameter set for the discontinuous function from Genz (1984)"
                "; constant shape and offset values"
            ),
            "declared_parameters": [
                {
                    "keyword": "aa",
                    "value": _get_aa_genz_1984,
                    "type": np.ndarray,
                    "description": "Shape parameter",
                },
                {
                    "keyword": "bb",
                    "value": _get_bb_genz_1984,
                    "type": np.ndarray,
                    "description": "Offset parameter",
                },
            ],
        },
    }
    _default_parameters_id = "Genz1984"

    evaluate = staticmethod(evaluate_discontinuous)  # type: ignore
