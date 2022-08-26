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
