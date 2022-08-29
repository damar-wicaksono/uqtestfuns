"""
Utility module for the test_functions sub-package.
"""
import numpy as np


def deg2rad(xx: np.ndarray) -> np.ndarray:
    """Convert angles given in degree to radians.

    Parameters
    ----------
    xx : np.ndarray
        Angles in degree.

    Returns
    -------
    np.ndarray
        Angles in radians.
    """
    yy = np.pi / 180.0 * xx

    return yy


def verify_input(xx: np.ndarray, num_cols: int):
    """Verify the number of columns of the input array.

    Parameters
    ----------
    xx : np.ndarray
        Array of input values with a shape of N-by-M, where N is the number
        of realizations and M is the spatial dimension.
    num_cols : int
        The expected number of columns in the input.

    Raises
    ------
    ValueError
        If the number of columns in the input is not equal to the expected
        number of columns.
    """
    if xx.shape[1] != num_cols:
        raise ValueError(
            f"Wrong dimensionality of the input array!"
            f"Expected {num_cols}, got {xx.shape[1]}."
        )
