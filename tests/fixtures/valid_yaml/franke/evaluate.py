import numpy as np


def franke_1(xx: np.ndarray):
    """Evaluate the (1st) Franke function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        Two-Dimensional input values given by N-by-2 arrays where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the (1st) Franke function evaluated
        on the input values.
        The output is a 1-dimensional array of length N.
    """

    xx0 = 9 * xx[:, 0]
    xx1 = 9 * xx[:, 1]

    # Compute the (first) Franke function
    term_1 = 0.75 * np.exp(-0.25 * ((xx0 - 2) ** 2 + (xx1 - 2) ** 2))
    term_2 = 0.75 * np.exp(
        -1.00 * ((xx0 + 1) ** 2 / 49.0 + (xx1 + 1) ** 2 / 10.0)
    )
    term_3 = 0.50 * np.exp(-0.25 * ((xx0 - 7) ** 2 + (xx1 - 3) ** 2))
    term_4 = 0.20 * np.exp(-1.00 * ((xx0 - 4) ** 2 + (xx1 - 7) ** 2))

    yy = term_1 + term_2 + term_3 - term_4

    return yy