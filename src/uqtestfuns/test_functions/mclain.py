"""
Module with an implementation of the McLain's test functions.

The McLain's test functions consists of five two-dimensional scalar-valued
functions. The functions were introduced in [1] in the context of drawing
contours from a given set of points.

There are five test functions in McLain's paper each models a mathematically
defined surface:

- S1: A part of a sphere
- S2: A steep hill rising from a plain
- S3: A less steep hill
- S4: A long narrow hill
- S5: A plateau and plain separated by a steep cliff

Four of the functions (S1-S3 and S5) appeared in modified forms in [2].

References
----------

1. D. H. McLain, "Drawing contours from arbitrary data points," The Computer
   Journal, vol. 17, no. 4, pp. 318-324, 1974.
   DOI: 10.1093/comjnl/17.4.318
2. Richard Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, Canada,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["McLainS1", "McLainS2", "McLainS3", "McLainS4", "McLainS5"]


AVAILABLE_INPUTS: ProbInputSpecs = {
    "McLain1974": {
        "function_id": "McLain",
        "description": (
            "Input specification for the McLain's test functions "
            "from McLain (1974)."
        ),
        "marginals": [  # From Ref. [1]
            {
                "name": "X1",
                "distribution": "uniform",
                "parameters": [1.0, 10.0],
                "description": None,
            },
            {
                "name": "X2",
                "distribution": "uniform",
                "parameters": [1.0, 10.0],
                "description": None,
            },
        ],
        "copulas": None,
    },
}

COMMON_METADATA = dict(
    _tags=["metamodeling"],
    _available_inputs=AVAILABLE_INPUTS,
    _available_parameters=None,
    _description="from McLain (1974)",
)


def evaluate_mclain_s1(xx: np.ndarray) -> np.ndarray:
    """Evaluate the McLain S1 function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the McLain S1 function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.sqrt(64 - (xx[:, 0] - 5.5) ** 2 - (xx[:, 1] - 5.5) ** 2)

    return yy


class McLainS1(UQTestFunFixDimABC):
    """A concrete implementation of the McLain S1 function.

    The function features a part of a sphere.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"McLain S1 function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_mclain_s1)  # type: ignore


def evaluate_mclain_s2(xx: np.ndarray) -> np.ndarray:
    """Evaluate the McLain S2 function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the McLain S2 function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(-1.0 * ((xx[:, 0] - 5) ** 2 + (xx[:, 1] - 5) ** 2))

    return yy


class McLainS2(UQTestFunFixDimABC):
    """A concrete implementation of the McLain S2 function.

    The function features a steep hill rising from a plain.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"McLain S2 function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_mclain_s2)  # type: ignore


def evaluate_mclain_s3(xx: np.ndarray) -> np.ndarray:
    """Evaluate the McLain S3 function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the McLain S3 function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(-0.25 * ((xx[:, 0] - 5) ** 2 + (xx[:, 1] - 5) ** 2))

    return yy


class McLainS3(UQTestFunFixDimABC):
    """A concrete implementation of the McLain S3 function.

    The function features a less steep hill (compared to S2).
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"McLain S3 function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_mclain_s3)  # type: ignore


def evaluate_mclain_s4(xx: np.ndarray) -> np.ndarray:
    """Evaluate the McLain S4 function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the McLain S4 function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.exp(
        -1
        * ((xx[:, 0] + xx[:, 1] - 11) ** 2 + (xx[:, 0] - xx[:, 1]) ** 2 / 10.0)
    )

    return yy


class McLainS4(UQTestFunFixDimABC):
    """A concrete implementation of the McLain S4 function.

    The function features a long narrow hill.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"McLain S4 function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_mclain_s4)  # type: ignore


def evaluate_mclain_s5(xx: np.ndarray) -> np.ndarray:
    """Evaluate the McLain S5 function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the McLain S5 function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.tanh(xx[:, 0] + xx[:, 1] - 11)

    return yy


class McLainS5(UQTestFunFixDimABC):
    """A concrete implementation of the McLain S5 function.

    The function features two plateaus separated by a steep cliff.
    """

    _tags = COMMON_METADATA["_tags"]
    _description = f"McLain S5 function {COMMON_METADATA['_description']}"
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]

    evaluate = staticmethod(evaluate_mclain_s5)  # type: ignore
