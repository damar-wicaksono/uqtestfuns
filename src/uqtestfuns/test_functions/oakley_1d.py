"""
Module with implementations of test functions from Oakley and O'Hagan (2002).

The 1D linear-cosine test function from Oakley and O'Hagan (2002)
(or `Oakley1D` function for short) was used in [1] as a test function
for illustrating metamodeling and uncertainty propagation approaches.

References
----------

1. Jeremy Oakley and Anthony O'Hagan, "Bayesian inference for the uncertainty
   distribution of computer model outputs," Biometrika , Vol. 89, No. 4,
   p. 769-784, 2002.
   DOI: 10.1093/biomet/89.4.769
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 1D Oakley-O'Hagan function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        1-Dimensional input values given by an N-by-1 array
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the 1D Oakley-O'Hagan function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 5 + xx[:, 0] + np.cos(xx[:, 0])

    return yy
