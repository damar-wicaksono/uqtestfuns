"""
Module with an implementation of the 2D function from Webster et al. (1996).

The two-dimensional function is polynomial with random input variables.
It was introduced in [1] and used to illustrate the construction of polynomial
chaos expansion metamodel.

References
----------
1. M. Webster, M. A. Tatang, and G. J. McRae, "Application of the probabilistic
   collocation method for an uncertainty analysis of a simple ocean model,"
   Massachusetts Institute of Technology, Cambridge, MA,
   Joint Program Report Series 4, 1996.
   [Online]. Available: http://globalchange.mit.edu/publication/15670
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 2D Webster function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 2D Webster function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = xx[:, 0] ** 2 + xx[:, 1] ** 3

    return yy
