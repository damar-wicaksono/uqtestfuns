"""
Module with an implementation of the Sobol-G test function.

The Sobol'-G function is an M-dimensional scalar-valued function.
It was introduced in [1] for testing numerical integration algorithms
(e.g., quasi-Monte-Carlo; see also for instance [2] and [3]).
The current form (and name) was from [4] and used in the context of global
sensitivity analysis. There, the function was generalized by introducing
a set of parameters that determines the importance of each input variable.
Later on, it becomes a popular testing function for global sensitivity analysis
methods; see, for instances, [5], [6], and [7].

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
"""
import numpy as np

from typing import List

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecVarDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["SobolG"]


def _create_sobol_input(spatial_dimension: int) -> List[UnivDistSpec]:
    """Construct an input instance for a given dimension according to [1].

    Parameters
    ----------
    spatial_dimension : int
        The number of marginals to be created.

    Returns
    -------
    List[UnivDistSpec]
        A list of M marginals as UnivariateInput instances to construct
        the MultivariateInput.
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivDistSpec(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[0.0, 1.0],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "Saltelli1995": ProbInputSpecVarDim(
        name="Sobol-G-Saltelli1995",
        description=(
            "Probabilistic input model for the Sobol'-G function "
            "from Saltelli and Sobol' (1995)"
        ),
        marginals_generator=_create_sobol_input,
        copulas=None,
    ),
}

DEFAULT_INPUT_SELECTION = "Saltelli1995"


def _get_params_saltelli_1995_1(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 1 in [4].

    Notes
    -----
    - The function was most probably first appear in its original form
      in [1] (without parameters).
    - With the selected parameters, all input variables are equally important.
    """
    yy = np.zeros(spatial_dimension)

    return yy


def _get_params_saltelli_1995_2(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 2 in [4].

    Notes
    -----
    - With the selected parameters, the first two input variables are
      important, one is moderately important, and the rest is non-influential.
    - Originally, the dimension is limited to 8-dimensions; if more dimensions
      are used then the remaining dimension is also non-influential.
    """
    yy = np.zeros(spatial_dimension)

    if spatial_dimension > 1:
        yy[1] = 0

    if spatial_dimension > 2:
        yy[2] = 3

    if spatial_dimension > 3:
        yy[3:] = 9

    return yy


def _get_params_saltelli_1995_3(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to example 3 in [4].

    Notes
    -----
    - With the selected parameters, the first input variable is the most
      important and the importance of the remaining variables is decreasing.
    - Originally, the dimension is limited to 20-dimensions; if more dimensions
      are used then the remaining dimension is also non-influential.
    - The parameter set is also used in [8].
    """
    yy = (np.arange(1, spatial_dimension + 1) - 1) / 2.0

    return yy


def _get_params_sobol_1998_1(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 1 in [2].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about 2^M [1].
    """
    yy = 0.01 * np.ones(spatial_dimension)

    return yy


def _get_params_sobol_1998_2(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 2 in [2].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about (1.5)^M [1];
      it's a bit slower than choice 1.
    """
    yy = np.ones(spatial_dimension)

    return yy


def _get_params_sobol_1998_3(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to choice 3 in [2].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows linearly as a function of dimension, i.e., 1 + (M/2) [1].
    """
    yy = np.arange(1, spatial_dimension + 1)

    return yy


def _get_params_sobol_1998_4(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol-G according to choice 4 in [2].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      is bounded at 1.0 [1].
    """
    yy = np.arange(1, spatial_dimension + 1) ** 2

    return yy


def _get_params_kucherenko_2011_2a(spatial_dimension: int) -> np.ndarray:
    """Construct a param. array for Sobol'-G according to problem 2A in [5]."""
    yy = np.zeros(spatial_dimension)
    if spatial_dimension >= 2:
        yy[2:] = 6.52

    return yy


def _get_params_kucherenko_2011_3b(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to problem 3B in [5].

    Notes
    -----
    - Using this choice of parameters, the supremum of the Sobol-G function
      grows exponentially as a function of dimension about (1.13)^M.
    """
    yy = 6.52 * np.ones(spatial_dimension)

    return yy


AVAILABLE_PARAMETERS = {
    "Saltelli1995-1": _get_params_saltelli_1995_1,
    "Saltelli1995-2": _get_params_saltelli_1995_2,
    "Saltelli1995-3": _get_params_saltelli_1995_3,
    "Sobol1998-1": _get_params_sobol_1998_1,
    "Sobol1998-2": _get_params_sobol_1998_2,
    "Sobol1998-3": _get_params_sobol_1998_3,
    "Sobol1998-4": _get_params_sobol_1998_4,
    "Kucherenko2011-2a": _get_params_kucherenko_2011_2a,
    "Kucherenko2011-3b": _get_params_kucherenko_2011_3b,
}

DEFAULT_PARAMETERS_SELECTION = "Saltelli1995-3"


def evaluate(xx: np.ndarray, parameters: np.ndarray):
    """Evaluate the Sobol-G function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    parameters : np.ndarray
        The parameters (i.e., coefficients) of the Sobol'-G function.

    Returns
    -------
    np.ndarray
        The output of the Sobol-G function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    aa = parameters
    yy = np.prod(((np.abs(4 * xx - 2) + aa) / (1 + aa)), axis=1)

    return yy


class SobolG(UQTestFunABC):
    """An implementation of the M-dimensional Sobol'-G test function."""

    _tags = ["sensitivity", "integration"]
    _description = "Sobol'-G function from Saltelli and Sobol' (1995)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = AVAILABLE_PARAMETERS
    _default_parameters = DEFAULT_PARAMETERS_SELECTION
    _default_spatial_dimension = None

    eval_ = staticmethod(evaluate)
