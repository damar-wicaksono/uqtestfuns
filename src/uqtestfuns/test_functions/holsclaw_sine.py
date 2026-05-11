"""
Module with an implementation of the Sine function from Holsclaw et al. (2013).

The one-dimensional, scalar-valued function was featured in [1] as an example
for Gaussian process metamodeling.

References
----------

1. T. Holsclaw, B. Sansó, H. K H. Lee, K. Heitmann, S. Habib, D. Higdon, and
   U. Alam, “Gaussian Process Modeling of Derivative Curves,” Technometrics,
   vol. 55, no. 1, pp. 57–67, 2013.
   DOI: 10.1080/00401706.2012.723918.
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Holsclaw sine function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 1)`` array of input values,
        where ``N`` is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length ``N``.
    """
    yy = xx[:, 0] * np.sin(xx[:, 0]) / 10

    return yy
