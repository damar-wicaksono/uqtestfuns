"""
Module with an implementation of the McLain's test functions.

The McLain's test functions consists of five two-dimensional scalar-valued
functions. The functions were introduced in [1] in the context of drawing
contours from a given set of points.

There are five test functions in McLain's paper each models a mathematically
defined surface:

- S1: A part of a sphere
- S2: A steep hill rising from a plain
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

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["McLainS1", "McLainS2", "McLainS5"]

INPUT_MARGINALS_MCLAIN1974 = [  # From Ref. [1]
    UnivDist(
        name="X1",
        distribution="uniform",
        parameters=[1.0, 10.0],
        description=None,
    ),
    UnivDist(
        name="X2",
        distribution="uniform",
        parameters=[1.0, 10.0],
        description=None,
    ),
]

AVAILABLE_INPUT_SPECS = {
    "McLain1974": {
        "name": "McLain-1974",
        "description": (
            "Input specification for the McLain's test functions "
            "from McLain (1974)."
        ),
        "marginals": INPUT_MARGINALS_MCLAIN1974,
        "copulas": None,
    }
}

DEFAULT_INPUT_SELECTION = "McLain1974"


COMMON_METADATA = dict(
    _TAGS=["metamodeling"],
    _AVAILABLE_INPUTS=tuple(AVAILABLE_INPUT_SPECS.keys()),
    _AVAILABLE_PARAMETERS=None,
    _DEFAULT_SPATIAL_DIMENSION=2,
    _DESCRIPTION="from McLain (1974)",
)


def _init(
    self,
    *,
    prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
    name: Optional[str] = None,
    rng_seed_prob_input: Optional[int] = None,
) -> None:
    """A common __init__ for all McLain's test functions."""
    # --- Arguments processing
    prob_input = create_prob_input_from_available(
        prob_input_selection,
        AVAILABLE_INPUT_SPECS,
        rng_seed=rng_seed_prob_input,
    )
    # Process the default name
    if name is None:
        name = self.__class__.__name__

    UQTestFunABC.__init__(self, prob_input=prob_input, name=name)


def _eval_s1(self, xx: np.ndarray):
    yy = np.sqrt(64 - (xx[:, 0] - 5.5) ** 2 - (xx[:, 1] - 5.5) ** 2)

    return yy


def _eval_s2(self, xx: np.ndarray):
    yy = np.exp(-1.0 * ((xx[:, 0] - 5) ** 2 + (xx[:, 1] - 5) ** 2))

    return yy


def _eval_s5(self, xx: np.ndarray):
    yy = np.tanh(xx[:, 0] + xx[:, 1] - 11)

    return yy


class McLainS1(UQTestFunABC):
    """A concrete implementation of the McLain S1 function."""

    _TAGS = COMMON_METADATA["_TAGS"]
    _AVAILABLE_INPUTS = COMMON_METADATA["_AVAILABLE_INPUTS"]
    _AVAILABLE_PARAMETERS = COMMON_METADATA["_AVAILABLE_PARAMETERS"]
    _DEFAULT_SPATIAL_DIMENSION = COMMON_METADATA["_DEFAULT_SPATIAL_DIMENSION"]
    _DESCRIPTION = f"McLain S1 function {COMMON_METADATA['_DESCRIPTION']}"

    __init__ = _init  # type: ignore
    evaluate = _eval_s1


class McLainS2(UQTestFunABC):
    """A concrete implementation of the McLain S2 function.

    The function features a steep hill rising from a plain.
    """

    _TAGS = COMMON_METADATA["_TAGS"]
    _AVAILABLE_INPUTS = COMMON_METADATA["_AVAILABLE_INPUTS"]
    _AVAILABLE_PARAMETERS = COMMON_METADATA["_AVAILABLE_PARAMETERS"]
    _DEFAULT_SPATIAL_DIMENSION = COMMON_METADATA["_DEFAULT_SPATIAL_DIMENSION"]
    _DESCRIPTION = f"McLain S1 function {COMMON_METADATA['_DESCRIPTION']}"

    __init__ = _init  # type: ignore
    evaluate = _eval_s2


class McLainS5(UQTestFunABC):
    """A concrete implementation of the McLain S5 function."""

    _TAGS = COMMON_METADATA["_TAGS"]
    _AVAILABLE_INPUTS = COMMON_METADATA["_AVAILABLE_INPUTS"]
    _AVAILABLE_PARAMETERS = COMMON_METADATA["_AVAILABLE_PARAMETERS"]
    _DEFAULT_SPATIAL_DIMENSION = COMMON_METADATA["_DEFAULT_SPATIAL_DIMENSION"]
    _DESCRIPTION = f"McLain S1 function {COMMON_METADATA['_DESCRIPTION']}"

    __init__ = _init  # type: ignore
    evaluate = _eval_s5
