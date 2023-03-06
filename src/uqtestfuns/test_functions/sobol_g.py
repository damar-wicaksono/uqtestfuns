"""
Module with an implementation of the Sobol-G test function.

The Sobol'-G function is an M-dimensional scalar-valued function.
It was introduced in [1] for testing numerical integration algorithms
(e.g., quasi-Monte-Carlo; see for instance [2].
Later on, it becomes a popular testing function for global sensitivity analysis
methods; see, for instances, [3], [4], and [5].

The parameters of the Sobol'-G function (i.e., the coefficients) determine
the importance of each input variable.
There are several sets of parameters used in the literature.

Notes
-----
- The parameters used in [3] and [4] correspond to
  the parameter choice 3 in [1].

References
----------
1. I. Radović, I. M. Sobol’, and R. F. Tichy, “Quasi-Monte Carlo Methods for
   Numerical Integration: Comparison of Different Low Discrepancy Sequences,”
   Monte Carlo Methods and Applications, vol. 2, no. 1, pp. 1–14, 1996.
   DOI: 10.1515/mcma.1996.2.1.1.
2. I. M. Sobol’, “On quasi-Monte Carlo integrations,” Mathematics and Computers
   in Simulation, vol. 47, no. 2–5, pp. 103–112, 1998.
   DOI: 10.1016/S0378-4754(98)00096-2
3. A. Marrel, B. Iooss, F. Van Dorpe, and E. Volkova, “An efficient
   methodology for modeling complex computer codes with Gaussian processes,”
   Computational Statistics & Data Analysis, vol. 52, no. 10,
   pp. 4731–4744, 2008.
   DOI: 10.1016/j.csda.2008.03.026
4. A. Marrel, B. Iooss, B. Laurent, and O. Roustant, “Calculations of Sobol
   indices for the Gaussian process metamodel,” Reliability Engineering &
   System Safety, vol. 94, no. 3, pp. 742–751, 2009.
    DOI: 10.1016/j.ress.2008.07.008
5. S. Kucherenko, B. Feil, N. Shah, and W. Mauntz, “The identification of
   model effective dimensions using global sensitivity analysis,”
   Reliability Engineering & System Safety, vol. 96, no. 4, pp. 440–449, 2011.
   DOI: 10.1016/j.ress.2010.11.003
6. T. Crestaux, J.-M. Martinez, O. Le Maître, and O. Lafitte, “Polynomial
   chaos expansion for uncertainties quantification and sensitivity analysis,”
   presented at the Fifth International Conference on Sensitivity Analysis
   of Model Output, 2007.
   Accessed: Jan. 25, 2023
   URL: http://samo2007.chem.elte.hu/lectures/Crestaux.pdf
"""
import numpy as np

from typing import List, Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import (
    create_prob_input_from_available,
    create_parameters_from_available,
)

__all__ = ["SobolG"]


def _create_sobol_input(spatial_dimension: int) -> List[UnivDist]:
    """Construct an input instance for a given dimension according to [1].

    Parameters
    ----------
    spatial_dimension : int
        The number of marginals to be created.

    Returns
    -------
    List[UnivDist]
        A list of M marginals as UnivariateInput instances to construct
        the MultivariateInput.
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivDist(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[0.0, 1.0],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "Radovic1996": {
        "name": "Sobol-G-Radovic-1996",
        "description": (
            "Probabilistic input model for the Sobol'-G function "
            "from Radović et al. (1996)."
        ),
        "marginals": _create_sobol_input,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "Radovic1996"


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


def _get_params_crestaux_2007(spatial_dimension: int) -> np.ndarray:
    """Construct a parameter array for Sobol'-G according to [6]."""
    yy = (np.arange(1, spatial_dimension + 1) - 1) / 2.0

    return yy


AVAILABLE_PARAMETERS = {
    "Sobol1998-1": _get_params_sobol_1998_1,
    "Sobol1998-2": _get_params_sobol_1998_2,
    "Sobol1998-3": _get_params_sobol_1998_3,
    "Sobol1998-4": _get_params_sobol_1998_4,
    "Kucherenko2011-2a": _get_params_kucherenko_2011_2a,
    "Kucherenko2011-3b": _get_params_kucherenko_2011_3b,
    "Crestaux2007": _get_params_crestaux_2007,
}

DEFAULT_PARAMETERS_SELECTION = "Crestaux2007"

# The dimension is variable, it requires a default for fallback
DEFAULT_DIMENSION_SELECTION = 2


class SobolG(UQTestFunABC):
    """A concrete implementation of the M-dimensional Sobol'-G function."""

    _TAGS = ["sensitivity"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = tuple(AVAILABLE_PARAMETERS.keys())

    _DEFAULT_SPATIAL_DIMENSION = None

    _DESCRIPTION = "Sobol'-G function from Radović et al. (1996)"

    def __init__(
        self,
        spatial_dimension: int = DEFAULT_DIMENSION_SELECTION,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        parameters_selection: Optional[str] = DEFAULT_PARAMETERS_SELECTION,
        name: Optional[str] = None,
    ):
        # --- Arguments processing
        if not isinstance(spatial_dimension, int):
            raise TypeError(
                f"Spatial dimension is expected to be of 'int'. "
                f"Got {type(spatial_dimension):!r} instead."
            )
        # Sobol-G is an M-dimensional test function, either given / use default
        # Create the input according to spatial dimension
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS, spatial_dimension
        )
        # Create the parameters according to spatial dimension
        parameters = create_parameters_from_available(
            parameters_selection, AVAILABLE_PARAMETERS, spatial_dimension
        )
        # Process the default name
        if name is None:
            name = SobolG.__name__

        super().__init__(
            prob_input=prob_input, parameters=parameters, name=name
        )

    def evaluate(self, xx: np.ndarray):
        """Evaluate the Sobol-G function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            M-Dimensional input values given by an N-by-M array where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the Sobol-G function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        params = self.parameters
        yy = np.prod(((np.abs(4 * xx - 2) + params) / (1 + params)), axis=1)

        return yy
