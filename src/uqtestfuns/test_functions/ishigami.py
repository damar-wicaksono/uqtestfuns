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

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import (
    create_prob_input_from_available,
    create_parameters_from_available,
)

__all__ = ["Ishigami"]


INPUT_MARGINALS_ISHIGAMI1991 = [
    UnivDist(
        name="X1",
        distribution="uniform",
        parameters=[-np.pi, np.pi],
        description="None",
    ),
    UnivDist(
        name="X2",
        distribution="uniform",
        parameters=[-np.pi, np.pi],
        description="None",
    ),
    UnivDist(
        name="X3",
        distribution="uniform",
        parameters=[-np.pi, np.pi],
        description="None",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "Ishigami1991": {
        "name": "Ishigami-1991",
        "description": (
            "Probabilistic input model for the Ishigami function "
            "from Ishigami and Homma (1991)."
        ),
        "marginals": INPUT_MARGINALS_ISHIGAMI1991,
        "copulas": None,
    }
}

DEFAULT_INPUT_SELECTION = "Ishigami1991"

AVAILABLE_PARAMETERS = {
    "Ishigami1991": (7, 0.05),  # from [1]
    "Sobol1999": (7, 0.1),  # from [2]
}

DEFAULT_PARAMETERS_SELECTION = "Ishigami1991"


class Ishigami(UQTestFunABC):
    """A concrete implementation of the Ishigami function."""

    _TAGS = ["sensitivity"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = tuple(AVAILABLE_PARAMETERS.keys())

    _DEFAULT_SPATIAL_DIMENSION = 3

    _DESCRIPTION = "Ishigami function from Ishigami and Homma (1991)"

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        parameters_selection: Optional[str] = DEFAULT_PARAMETERS_SELECTION,
        name: Optional[str] = None,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )
        # Ishigami supports several different parameterizations
        parameters = create_parameters_from_available(
            parameters_selection, AVAILABLE_PARAMETERS
        )
        # Process the default name
        if name is None:
            name = Ishigami.__name__

        super().__init__(
            prob_input=prob_input, parameters=parameters, name=name
        )

    def evaluate(self, xx):
        """Evaluate the Ishigami function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            3-Dimensional input values given by N-by-3 arrays where
            N is the number of input values.
        params : tuple
            Tuple of two values as the parameters of the function.

        Returns
        -------
        np.ndarray
            The output of the Ishigami function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        # Compute the Ishigami function
        parameters = self.parameters
        term_1 = np.sin(xx[:, 0])
        term_2 = parameters[0] * np.sin(xx[:, 1]) ** 2
        term_3 = parameters[1] * xx[:, 2] ** 4 * np.sin(xx[:, 0])

        yy = term_1 + term_2 + term_3

        return yy
