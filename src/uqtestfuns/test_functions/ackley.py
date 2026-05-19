"""
Module with an implementation of the M-dimensional Ackley function.

The Ackley function  is an $M$-dimensional scalar-valued function.
The function was first introduced in [1] as a test function for optimization
algorithms,
Originally presented as a two-dimensional function, it was later generalized
by Bäck and Schwefel [2].

References
----------

1. D. H. Ackley, A Connectionist Machine for Genetic Hillclimbing,
   The Kluwer International Series in Engineering and Computer Science vol. 28.
   Boston, MA: Springer US, 1987.
   DOI: 10.1007/978-1-4613-1997-9
2. T. Bäck and H.-P. Schwefel, “An overview of evolutionary algorithms for
   parameter optimization,” Evolutionary Computation,
   vol. 1, no. 1, pp. 1–23, 1993.
   DOI: 10.1162/evco.1993.1.1.1.
"""

import numpy as np


def evaluate(xx: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Evaluate the Ackley function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-M array where
        N is the number of input values.
    a : float
        Height of the ridges surrounding the minimum.
    b : float
        Decay rate of the Euclidean distance.
    c : float
        Scaling constant for the cosine term.

    Returns
    -------
    np.ndarray
        The output of the Ackley function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """

    m = xx.shape[1]

    # Compute the Ackley function
    term_1 = -1 * a * np.exp(-1 * b * np.sqrt(np.sum(xx**2, axis=1) / m))
    term_2 = -1 * np.exp(np.sum(np.cos(c * xx), axis=1) / m)

    yy = term_1 + term_2 + a + np.exp(1)

    return yy
