import numpy as np


def evaluate_curved(xx: np.ndarray) -> np.ndarray:
    """Evaluate the highly-curved function from Dette and Pepelyshev (2010).

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-3 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    term_1 = 4 * (xx[:, 0] - 2 + 8 * xx[:, 1] - 8 * xx[:, 1] ** 2)
    term_2 = (3 - 4 * xx[:, 1]) ** 2
    term_3 = (16 * (xx[:, 2] + 1) ** 0.5) * (2 * xx[:, 2] - 1) ** 2

    return term_1 + term_2 + term_3


def evaluate_8d(xx: np.ndarray) -> np.ndarray:
    """Evaluate the 8D function from Dette and Pepelyshev (2010).

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-8 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    term_1 = evaluate_curved(xx)
    term_2 = np.zeros(len(xx))
    for j in range(3, xx.shape[1]):
        term_2 += (j + 1) * np.log(1 + np.sum(xx[:, 2:j], axis=1))

    return term_1 + term_2
