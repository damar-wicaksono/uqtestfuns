"""
Module with an implementation of the Borehole function.

The Borehole test function [1] is an 8-dimensional scalar-valued function
that models water flow through a borehole that is drilled from
the ground surface through two aquifers.

The unit of the output is [m^3/year].

References
----------

1. W. V. Harper and S. K. Gupta, “Sensitivity/Uncertainty Analysis of
   a Borehole Scenario Comparing Latin Hypercube Sampling and
   Deterministic Sensitivity Approaches”, Office of Nuclear Waste
   Isolation, Battelle Memorial Institute, Columbus, Ohio,
   BMI/ONWI-516, 1983.
   URL: https://inldigitallibrary.inl.gov/PRR/84393.pdf
2. M. D. Morris, T. J. Mitchell, and D. Ylvisaker, “Bayesian design and
   analysis of computer experiments: Use of derivatives in surface
   prediction,” Technometrics, vol. 35, no. 3, pp. 243–255, 1993.
   DOI:10.1080/00401706.1993.10485320
"""
import numpy as np

from .utils import verify_spatial_dimension

DEFAULT_NAME = "Borehole"

# From Ref. 1
DEFAULT_INPUT_DICTS = [
    {
        "name": "rw",
        "distribution": "normal",
        "parameters": [0.10, 0.0161812],
        "description": "radius of the borehole [m]",
    },
    {
        "name": "r",
        "distribution": "lognormal",
        "parameters": [7.71, 1.0056],
        "description": "radius of influence [m]",
    },
    {
        "name": "Tu",
        "distribution": "uniform",
        "parameters": [63070.0, 115600.0],
        "description": "transmissivity of upper aquifer [m^2/year]",
    },
    {
        "name": "Hu",
        "distribution": "uniform",
        "parameters": [990.0, 1100.0],
        "description": "potentiometric head of upper aquifer [m]",
    },
    {
        "name": "Tl",
        "distribution": "uniform",
        "parameters": [63.1, 116.0],
        "description": "transmissivity of lower aquifer [m^2/year]",
    },
    {
        "name": "Hl",
        "distribution": "uniform",
        "parameters": [700.0, 820.0],
        "description": "potentiometric head of lower aquifer [m]",
    },
    {
        "name": "L",
        "distribution": "uniform",
        "parameters": [1120.0, 1680.0],
        "description": "length of the borehole [m]",
    },
    {
        "name": "Kw",
        "distribution": "uniform",
        "parameters": [9985.0, 12045.0],
        "description": "hydraulic conductivity of the borehole [m/year]",
    },
]

# From Ref. 2
ALTERNATIVE_INPUT_DICTS = [_.copy() for _ in DEFAULT_INPUT_DICTS]
ALTERNATIVE_INPUT_DICTS[0:2] = [
    {
        "name": "rw",
        "distribution": "uniform",
        "parameters": [0.05, 0.15],
        "description": "radius of the borehole [m]",
    },
    {
        "name": "r",
        "distribution": "uniform",
        "parameters": [100, 50000],
        "description": "radius of influence [m]",
    },
]

DEFAULT_PARAMETERS = None

SPATIAL_DIMENSION = len(DEFAULT_INPUT_DICTS)


def get_default_input(spatial_dimension: int = None):
    """Get the default list of dictionaries to construct the Input instance."""
    verify_spatial_dimension(
        spatial_dimension,
        SPATIAL_DIMENSION,
        DEFAULT_NAME,
    )

    return DEFAULT_INPUT_DICTS


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Borehole function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        8-Dimensional input values given by N-by-8 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Borehole function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    # Compute the Borehole function
    nom = 2 * np.pi * xx[:, 2] * (xx[:, 3] - xx[:, 5])
    denom_1 = np.log(xx[:, 1] / xx[:, 0])
    denom_2 = (
        2
        * xx[:, 6]
        * xx[:, 2]
        / (np.log(xx[:, 1] / xx[:, 0]) * xx[:, 0] ** 2 * xx[:, 7])
    )
    denom_3 = xx[:, 2] / xx[:, 4]

    yy = nom / (denom_1 * (1 + denom_2 + denom_3))

    return yy
