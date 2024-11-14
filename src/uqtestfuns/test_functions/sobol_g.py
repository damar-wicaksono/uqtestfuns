"""
Module with an implementation of the Sobol-G test function.

The Sobol'-G function is an M-dimensional scalar-valued function.
It was introduced in [1] for testing numerical integration algorithms
(e.g., quasi-Monte-Carlo; see also for instance [2] and [3]).
The current form (and name) was from [4] and used in the context of global
sensitivity analysis. There, the function was generalized by introducing
a set of parameters that determines the importance of each input variable.
Later on, it becomes a popular testing function for global sensitivity analysis
methods; see, for instances, [5], [6], [7], and [9].

There are several sets of parameters used in the literature.

Notes
-----
- The parameters used in [5] and [6] correspond to
  the parameter choice 3 in [3].

References
----------

1. Paul Bratley, Bennet L. Fox, and Harald Niederreiter, "Implementation and
   tests of low-discrepancy sequences," ACM Transactions on Modeling and
   Computer Simulation, vol. 2, no. 3, pp. 195-213, 1992.
   DOI:10.1145/146382.146385
2. I. Radović, I. M. Sobol’, and R. F. Tichy, “Quasi-Monte Carlo Methods for
   Numerical Integration: Comparison of Different Low Discrepancy Sequences,”
   Monte Carlo Methods and Applications, vol. 2, no. 1, pp. 1–14, 1996.
   DOI: 10.1515/mcma.1996.2.1.1.
3. I. M. Sobol’, “On quasi-Monte Carlo integrations,” Mathematics and Computers
   in Simulation, vol. 47, no. 2–5, pp. 103–112, 1998.
   DOI: 10.1016/S0378-4754(98)00096-2
4. A. Saltelli and I. M. Sobol’, “About the use of rank transformation in
   sensitivity analysis of model output,” Reliability Engineering
   & System Safety, vol. 50, no. 3, pp. 225–239, 1995.
   DOI: 10.1016/0951-8320(95)00099-2.
5. A. Marrel, B. Iooss, F. Van Dorpe, and E. Volkova, “An efficient
   methodology for modeling complex computer codes with Gaussian processes,”
   Computational Statistics & Data Analysis, vol. 52, no. 10,
   pp. 4731–4744, 2008.
   DOI: 10.1016/j.csda.2008.03.026
6. A. Marrel, B. Iooss, B. Laurent, and O. Roustant, “Calculations of Sobol
   indices for the Gaussian process metamodel,” Reliability Engineering &
   System Safety, vol. 94, no. 3, pp. 742–751, 2009.
    DOI: 10.1016/j.ress.2008.07.008
7. S. Kucherenko, B. Feil, N. Shah, and W. Mauntz, “The identification of
   model effective dimensions using global sensitivity analysis,”
   Reliability Engineering & System Safety, vol. 96, no. 4, pp. 440–449, 2011.
   DOI: 10.1016/j.ress.2010.11.003
8. T. Crestaux, J.-M. Martinez, O. Le Maître, and O. Lafitte, “Polynomial
   chaos expansion for uncertainties quantification and sensitivity analysis,”
   presented at the Fifth International Conference on Sensitivity Analysis
   of Model Output, 2007.
   Accessed: Jan. 25, 2023
   URL: http://samo2007.chem.elte.hu/lectures/Crestaux.pdf
9. X. Sun, B. Croke, A. Jakeman, S. Roberts, "Benchmarking Active Subspace
   methods of global sensitivity analysis against variance-based Sobol’
   and Morris methods with established test functions," Environmental Modelling
   & Software, vol. 149, p. 105310, 2022.
   DOI: 10.1016/j.envsoft.2022.105310
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs, FunParamSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunVarDimABC

__all__ = ["SobolG"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Saltelli1995": {
        "function_id": "SobolG",
        "description": (
            "Probabilistic input model for the Sobol'-G function "
            "from Saltelli and Sobol' (1995)"
        ),
        "marginals": [
            {
                "name": "X",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "Saltelli1995"


def _get_params_saltelli_1995_1(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 1 in [4].

    Notes
    -----
    - The function was most probably first appear in its original form
      in [1] (without parameters).
    - With the selected parameters, all input variables are equally important.
    """
    yy = np.zeros(input_dimension)

    return yy


def _get_params_saltelli_1995_2(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 2 in [4].

    Notes
    -----
    - With the selected parameters, the first two input variables are
      important, one is moderately important, and the rest is non-influential.
    - Originally, the dimension is limited to 8-dimensions; if more dimensions
      are used then the remaining dimension is also non-influential.
    """
    yy = np.zeros(input_dimension)

    if input_dimension > 1:
        yy[1] = 0

    if input_dimension > 2:
        yy[2] = 3

    if input_dimension > 3:
        yy[3:] = 9

    return yy


def _get_params_saltelli_1995_3(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 3 in [4].

    Notes
    -----
    - With the selected parameters, the first input variable is the most
      important and the importance of the remaining variables is decreasing.
    - Originally, the dimension is limited to 20-dimensions; if more dimensions
      are used then the remaining dimension is also non-influential.
    - The parameter set is also used in [8].
    """
    yy = (np.arange(1, input_dimension + 1) - 1) / 2.0

    return yy


def _get_params_sobol_1998_1(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 1 in [3].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about 2^M.
    """
    yy = 0.01 * np.ones(input_dimension)

    return yy


def _get_params_sobol_1998_2(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 2 in [3].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about (1.5)^M;
      it's a bit slower than choice 1.
    """
    yy = np.ones(input_dimension)

    return yy


def _get_params_sobol_1998_3(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 3 in [3].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows linearly as a function of dimension, i.e., 1 + (M/2).
    """
    yy = np.arange(1, input_dimension + 1)

    return yy


def _get_params_sobol_1998_4(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol-G according to choice 4 in [3].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      is bounded at 1.0.
    """
    yy = np.arange(1, input_dimension + 1) ** 2

    return yy


def _get_params_kucherenko_2011_2a(input_dimension: int) -> np.ndarray:
    """Construct a param. array for Sobol'-G according to problem 2A in [7]."""
    yy = np.zeros(input_dimension)
    if input_dimension >= 2:
        yy[2:] = 6.52

    return yy


def _get_params_kucherenko_2011_3b(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to problem 3B in [7].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about (1.13)^M.
    """
    yy = 6.52 * np.ones(input_dimension)

    return yy


def _get_params_sun_2022(input_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to Sec. 3. 2. [9].

    Notes
    -----
    - The length of the array in [9] is originally seven following
      a 7-dimensional function. If input dimension is larger than 7,
      then the remaining coefficients are extrapolated
      from the last available value.
    """
    aa = np.array([0.0, 1.0, 4.5, 9.0, 99, 99, 99])

    if input_dimension > len(aa):
        aa_ext = 99 * np.ones(input_dimension - len(aa))
        aa = np.append(aa, aa_ext)

    return aa[:input_dimension]


AVAILABLE_PARAMETERS: FunParamSpecs = {
    "Saltelli1995-1": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Saltelli and Sobol' "
            "(1995), example 1; all input variables are equally important"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_saltelli_1995_1,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Saltelli1995-2": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Saltelli and Sobol' "
            "(1995), example 2; the first two input variables are the most "
            "important and the rest are non-influential"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_saltelli_1995_2,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Saltelli1995-3": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Saltelli and Sobol' "
            "(1995), example 3; the first input variable is the most "
            "important and the importance of the remaining variables is "
            "decreasing"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_saltelli_1995_3,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Sobol1998-1": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Sobol' (1998)"
            "(1995), choice 1; the supremum of the function grows "
            "exponentially as a function of dimension about 2^M"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_sobol_1998_1,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Sobol1998-2": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Sobol' (1998)"
            "(1995), choice 2; the supremum of the function grows "
            "exponentially as a function of dimension about (1.5)^M"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_sobol_1998_2,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Sobol1998-3": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Sobol' (1998)"
            "(1995), choice 3; the supremum of the function grows "
            "linearly as a function of dimension, i.e., 1 + M / 2"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_sobol_1998_3,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Sobol1998-4": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Sobol' (1998)"
            "(1995), choice 4; the supremum of the function is bounded at 1.0"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_sobol_1998_4,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Kucherenko2011-2a": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Kucherenko et al. "
            "(2011), problem 2A"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_kucherenko_2011_2a,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Kucherenko2011-3b": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Kucherenko et al. "
            "(2011), problem 3B; the supremum of the function grows "
            "exponentially as a function of dimension about (1.13)^M"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_kucherenko_2011_3b,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
    "Sun2022": {
        "function_id": "SobolG",
        "description": (
            "Parameter set for the Sobol-G function from Sun et al. "
            "(2022), Section 3.2"
        ),
        "declared_parameters": [
            {
                "keyword": "aa",
                "value": _get_params_sun_2022,
                "type": np.ndarray,
                "description": "Coefficients 'a'",
            },
        ],
    },
}

DEFAULT_PARAMETERS_SELECTION = "Saltelli1995-3"


def evaluate(xx: np.ndarray, aa: np.ndarray):
    """Evaluate the Sobol-G function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    aa : np.ndarray
        The vector of parameters (i.e., coefficients) of the Sobol'-G function;
        the length of the vector is the same as the number of input dimensions.

    Returns
    -------
    np.ndarray
        The output of the Sobol-G function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.prod(((np.abs(4 * xx - 2) + aa) / (1 + aa)), axis=1)

    return yy


class SobolG(UQTestFunVarDimABC):
    """An implementation of the M-dimensional Sobol'-G test function."""

    _tags = ["sensitivity", "integration"]
    _description = "Sobol'-G function from Saltelli and Sobol' (1995)"
    _available_inputs = AVAILABLE_INPUTS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters_id = DEFAULT_PARAMETERS_SELECTION

    evaluate = staticmethod(evaluate)  # type: ignore
