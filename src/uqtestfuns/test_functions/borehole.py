"""
Borehole function from Harper and Gupta (1983).

The function models water flow through a borehole drilled
from the ground surface through two aquifers. Output unit is m^3/year.

References
----------

1. W. V. Harper and S. K. Gupta, "Sensitivity/Uncertainty Analysis of
   a Borehole Scenario Comparing Latin Hypercube Sampling and
   Deterministic Sensitivity Approaches", Office of Nuclear Waste
   Isolation, Battelle Memorial Institute, Columbus, Ohio,
   BMI/ONWI-516, 1983.
   URL: https://inldigitallibrary.inl.gov/PRR/84393.pdf
2. M. D. Morris, T. J. Mitchell, and D. Ylvisaker, "Bayesian design and
   analysis of computer experiments: Use of derivatives in surface
   prediction," Technometrics, vol. 35, no. 3, pp. 243-255, 1993.
   DOI: 10.1080/00401706.1993.10485320
"""

import numpy as np


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
