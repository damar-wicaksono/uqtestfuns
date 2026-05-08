"""
Module with implementations of the Franke test functions from Franke (1979).

Six two-dimensional scalar-valued functions for scattered data interpolation
and metamodeling benchmarking. Functions 2, 4, 5, and 6 are adapted from
McLain (1974) (S5, S3, S2, and S1 respectively).

While the Franke's original report [1] contains in total six two-dimensional
test functions, only the first Franke function is commonly known
as the "Franke function".

References
----------

1. R. Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, CA,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
2. B. Haaland and P. Z. G. Qian, "Accurate emulators for large-scale
   computer experiments," The Annals of Statistics, vol. 39, no. 6,
   pp. 2974-3002, 2011.
   DOI: 10.1214/11-AOS929
3. D. H. McLain, "Drawing contours from arbitrary data points," The Computer
   Journal, vol. 17, no. 4, pp. 318-324, 1974.
   DOI: 10.1093/comjnl/17.4.318
"""

import numpy as np


def franke_1(xx: np.ndarray) -> np.ndarray:
    """Evaluate the (1st) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 2)`` array of input values.

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N``.
    """
    xx0 = 9 * xx[:, 0]
    xx1 = 9 * xx[:, 1]

    term_1 = 0.75 * np.exp(-0.25 * ((xx0 - 2) ** 2 + (xx1 - 2) ** 2))
    term_2 = 0.75 * np.exp(
        -1.00 * ((xx0 + 1) ** 2 / 49.0 + (xx1 + 1) ** 2 / 10.0)
    )
    term_3 = 0.50 * np.exp(-0.25 * ((xx0 - 7) ** 2 + (xx1 - 3) ** 2))
    term_4 = 0.20 * np.exp(-1.00 * ((xx0 - 4) ** 2 + (xx1 - 7) ** 2))

    return term_1 + term_2 + term_3 - term_4