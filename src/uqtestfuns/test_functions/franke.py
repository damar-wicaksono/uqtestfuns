"""
Module with an implementation of the Franke's test function.

The Franke's test functions are a set of six two-dimensional scalar-valued
functions. The functions were introduced in [1] in the context of
scattered data interpolation and was used in the context of metamodeling
in [2].

The six functions are:

- (1st) Franke function: Two Gaussian peaks and a Gaussian dip on a surface
  slopping down toward the upper right boundary.
- (2nd) Franke function: Two nearly flat regions joined by a sharp rise running
  diagonally.
- (3rd) Franke function: A saddle shaped surface.
- (4th) Franke function: A Gaussian hill that slopes off in a gentle fashion.
- (5th) Franke function: A steep Gaussian hill which becomes almost zero at
  the boundaries.
- (6th) Franke function: A part of a sphere.

Four of the Franke functions, namely the 2nd, 4th, 5th, and 6th are modified
from [3] (namely, S5, S3, S2 and S1, respectively).

While the Franke's original report [1] contains in total six two-dimensional
test functions, only the first Franke function is commonly known
as the "Franke function".

References
----------

1. Richard Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, Canada,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
2. Ben Haaland and Peter Z. G. Qian, “Accurate emulators for large-scale
   computer experiments,” The Annals of Statistics, vol. 39, no. 6,
   pp. 2974-3002, 2011. DOI: 10.1214/11-AOS929
3. D. H. McLain, "Drawing contours from arbitrary data points," The Computer
   Journal, vol. 17, no. 4, pp. 318-324, 1974.
   DOI: 10.1093/comjnl/17.4.318
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["Franke1", "Franke2", "Franke3", "Franke4", "Franke5", "Franke6"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "Franke1979": {
        "function_id": "Franke",
        "description": (
            "Input specification for the test functions from Franke (1979)."
        ),
        "marginals": [
            {
                "name": "X1",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "uniform",
                "parameters": [0.0, 1.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}


DEFAULT_INPUT_SELECTION = "Franke1979"

COMMON_METADATA = dict(
    _tags=["metamodeling"],
    _available_inputs=AVAILABLE_INPUTS,
    _available_parameters=None,
    _description="from Franke (1979)",
)


def evaluate_franke1(xx: np.ndarray):
    """Evaluate the (1st) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (1st) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """

    xx0 = 9 * xx[:, 0]
    xx1 = 9 * xx[:, 1]

    # Compute the (first) Franke function
    term_1 = 0.75 * np.exp(-0.25 * ((xx0 - 2) ** 2 + (xx1 - 2) ** 2))
    term_2 = 0.75 * np.exp(
        -1.00 * ((xx0 + 1) ** 2 / 49.0 + (xx1 + 1) ** 2 / 10.0)
    )
    term_3 = 0.50 * np.exp(-0.25 * ((xx0 - 7) ** 2 + (xx1 - 3) ** 2))
    term_4 = 0.20 * np.exp(-1.00 * ((xx0 - 4) ** 2 + (xx1 - 7) ** 2))

    yy = term_1 + term_2 + term_3 - term_4

    return yy


class Franke1(UQTestFunFixDimABC):
    """A concrete implementation of the (1st) Franke function.

    The function features two Gaussian peaks and a Gaussian dip.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(1st) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke1)  # type: ignore


def evaluate_franke2(xx: np.ndarray):
    """Evaluate the (2nd) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (2nd) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (np.tanh(9 * (xx[:, 1] - xx[:, 0])) + 1) / 9.0

    return yy


class Franke2(UQTestFunFixDimABC):
    """A concrete implementation of the (2nd) Franke function.

    The function features two plateaus joined by a steep hill.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(2nd) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke2)  # type: ignore


def evaluate_franke3(xx: np.ndarray):
    """Evaluate the (3rd) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (3rd) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    term_1 = 1.25 + np.cos(5.4 * xx[:, 1])
    term_2 = 6 * (1 + (3 * xx[:, 0] - 1) ** 2)

    yy = term_1 / term_2

    return yy


class Franke3(UQTestFunFixDimABC):
    """A concrete implementation of the (3rd) Franke function.

    The function features a saddle shaped surface.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(3rd) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke3)  # type: ignore


def evaluate_franke4(xx: np.ndarray):
    """Evaluate the (4th) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (4th) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (
        np.exp(-81.0 / 16.0 * ((xx[:, 0] - 0.5) ** 2 + (xx[:, 1] - 0.5) ** 2))
        / 3.0
    )

    return yy


class Franke4(UQTestFunFixDimABC):
    """A concrete implementation of the (4th) Franke function.

    The function features a gentle Gaussian hill.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(4th) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke4)  # type: ignore


def evaluate_franke5(xx: np.ndarray):
    """Evaluate the (5th) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (5th) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (
        np.exp(-81.0 / 4.0 * ((xx[:, 0] - 0.5) ** 2 + (xx[:, 1] - 0.5) ** 2))
        / 3.0
    )

    return yy


class Franke5(UQTestFunFixDimABC):
    """A concrete implementation of the (5th) Franke function.

    The function features a steep Gaussian hill.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(5th) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke5)  # type: ignore


def evaluate_franke6(xx: np.ndarray):
    """Evaluate the (6th) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (6th) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = (
        np.sqrt(64 - 81 * ((xx[:, 0] - 0.5) ** 2 + (xx[:, 1] - 0.5) ** 2))
        / 9.0
        - 0.5
    )

    return yy


class Franke6(UQTestFunFixDimABC):
    """A concrete implementation of the (6th) Franke function.

    The function features a part of a sphere.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"(6th) Franke function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_franke6)  # type: ignore
