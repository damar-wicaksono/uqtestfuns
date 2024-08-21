"""
This module contains a collection of the default basis functions
for the meta.
"""

import numpy as np


__all__ = ["BASIS_BY_ID"]


def linear(xx: np.ndarray) -> np.ndarray:
    """Compute the linear function on a set of 1-dimensional points."""
    return xx


def quadratic(xx: np.ndarray) -> np.ndarray:
    """Compute the quadratic function on a set of 1-dimensional points."""
    return xx**2


def cubic(xx: np.ndarray) -> np.ndarray:
    """Compute the cubic function on a set of 1-dimensional points."""
    return xx**3


def exponential(xx: np.ndarray) -> np.ndarray:
    """Compute the exponential function on a set of 1-dimensional points."""
    yy = (np.exp(xx) - 1) / (np.exp(1) - 1)

    return yy


def periodic(xx: np.ndarray) -> np.ndarray:
    """Compute the sine periodic function on a set of 1-dimensional points."""
    yy = 0.5 * np.sin(2 * np.pi * xx)

    return yy


def discontinuous(xx: np.ndarray) -> np.ndarray:
    """Compute the discontinuous function on a set of 1-dimensional points."""
    yy = np.zeros(xx.shape)
    yy[xx > 0.5] = 1.0

    return yy


def null(xx: np.ndarray) -> np.ndarray:
    """Compute the null function on a set of 1-dimensional points."""
    yy = np.zeros(xx.shape)

    return yy


def non_monotonic(xx: np.ndarray) -> np.ndarray:
    """Compute the parabola function on a set of 1-dimensional points."""
    yy = 4 * (xx - 0.5) ** 2

    return yy


def inverse(xx: np.ndarray) -> np.ndarray:
    """Compute the inverse function on a set of 1-dimensional points."""
    yy = (10 - 1 / 1.1) ** (-1) * (xx + 0.1) ** (-1)

    return yy


def trigonometric(xx: np.ndarray) -> np.ndarray:
    """Compute the trigonometric function on a set of 1-dimensional points."""
    yy = np.cos(xx)

    return yy


BASIS_BY_ID = {
    0: linear,
    1: quadratic,
    2: cubic,
    3: exponential,
    4: periodic,
    5: discontinuous,
    6: null,
    7: non_monotonic,
    8: inverse,
    9: trigonometric,
}
