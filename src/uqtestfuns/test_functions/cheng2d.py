"""
Module with an implementation of the 2D function from Cheng and Sandu (2010).

The two-dimensional trigonometric-exponential function was used in [1]
as an example for metamodeling using polynomial chaos expansion.

References
----------
1. H. Cheng and A. Sandu, “Collocation least-squares polynomial chaos method,”
   in Proceedings of the 2010 Spring Simulation Multiconference, Orlando,
   Florida: Society for Computer Simulation International, 2010, pp. 1–6.
   DOI: 10.1145/1878537.1878621.
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 2D test function from Cheng and Sandu (2010).

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = np.cos(np.sum(xx, axis=1)) * np.exp(np.prod(xx, axis=1))

    return yy
