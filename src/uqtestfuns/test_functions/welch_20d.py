"""
Module with an implementation of the Welch et al. (1992) test function.

The Welch1992 test function is a 20-dimensional scalar-valued function.
The function features some strong non-linear effects as well as some pair
interaction effects. Furthermore, two input variables (namely x8 and x16)
are inert.

The function was introduced in [1] as a test function for metamodeling and
sensitivity analysis purposes. The function is also suitable for testing
multi-dimensional integration algorithms.

References
----------

1. William J. Welch, Robert J. Buck, Jerome Sacks, Henry P. Wynn,
   Toby J. Mitchell, and Max D. Morris, "Screening, predicting, and computer
   experiments," Technometrics, vol. 34, no. 1, pp. 15-25, 1992.
   DOI: 10.2307/1269548
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Welch et al. (1992) function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 20)`` array of input values,
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.

    Notes
    -----
    - The input variables xx[:, 7] (x8) and xx[:, 15] (x16) are inert and
      therefore, do not appear in the computation below.
    """
    yy = (
        (5 * xx[:, 11]) / (1 + xx[:, 0])
        + 5 * (xx[:, 3] - xx[:, 19]) ** 2
        + xx[:, 4]
        + 40 * xx[:, 18] ** 3
        - 5 * xx[:, 18]
        + 0.05 * xx[:, 1]
        + 0.08 * xx[:, 2]
        - 0.03 * xx[:, 5]
        + 0.03 * xx[:, 6]
        - 0.09 * xx[:, 8]
        - 0.01 * xx[:, 9]
        - 0.07 * xx[:, 10]
        + 0.25 * xx[:, 12] ** 2
        - 0.04 * xx[:, 13]
        + 0.06 * xx[:, 14]
        - 0.01 * xx[:, 16]
        - 0.03 * xx[:, 17]
    )

    return yy
