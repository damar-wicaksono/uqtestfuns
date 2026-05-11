"""
Module with an implementation of the Sine function from Higdon (2002).

The one-dimensional, scalar-valued function was featured in [1] as an example
for a multi-resolution spatial modeling technique.

References
----------

1. D. Higdon, “Space and Space-Time Modeling using Process Convolutions,”
   in Quantitative Methods for Current Environmental Issues, C. W. Anderson,
   V. Barnett, P. C. Chatwin, and A. H. El-Shaarawi, Eds.,
   London: Springer London, 2002, pp. 37–56.
   DOI: 10.1007/978-1-4471-0657-9_2.

"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Higdon sine function on a set of input values.

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
    xx_ = xx[:, 0]
    yy = np.sin(2 * np.pi * xx_ / 10) + 0.2 * np.sin(2 * np.pi * xx_ / 2.5)

    return yy
