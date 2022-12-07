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


def verify_spatial_dimension(
    spatial_dimension: int,
    default_spatial_dimension: int,
    function_name: str,
):
    """Verify the spatial dimension given a default value."""
    if (
        spatial_dimension is not None
        and spatial_dimension != default_spatial_dimension
    ):
        raise ValueError(
            f"Spatial dimension for the {function_name} test function "
            f"is fixed to {default_spatial_dimension}."
        )
