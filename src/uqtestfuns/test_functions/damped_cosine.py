"""
Module with an implementation of the test function from Santner et al. (2018).

The function is a one-dimensional damped cosine scalar-valued function
used in [1] as a test function for metamodeling exercises.

References
----------

1. Thomas J. Santner, Brian J. Williams, and William I. Notz, "The Design
   and Analysis of Computer Experiments," Springer New York, 2018.
   DOI: 10.1007/978-1-4939-8847-1
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 1D damped cosine function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N``.
    """
    yy = np.exp(-1.4 * xx[:, 0]) * np.cos(3.5 * np.pi * xx[:, 0])

    return yy
