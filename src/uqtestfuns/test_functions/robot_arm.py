"""
Module with an implementation of the Robot Arm test function.

The Robot Arm test function is an eight-dimensional scalar-valued test function
typically used in metamodeling exercises (see, for example, [1] and [2]).

References
----------

1. J. An and A. Owen, “Quasi-regression,” Journal of Complexity, vol. 17,
   no. 4, pp. 588–607, 2001.
   DOI: 10.1006/jcom.2001.0588
2. M. A. Bouhlel, J. T. Hwang, N. Bartoli, R. Lafage, J. Morlier,
   and J. R. R. A. Martins, “A Python surrogate modeling framework with
   derivatives,” Advances in Engineering Software, vol. 135, p. 102662, 2019.
   DOI: 10.1016/j.advengsoft.2019.03.005
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Robot Arm test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        8-Dimensional input values given by an N-by-8 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    # Rearrange inputs
    ll = xx[:, :4]  # Segment lengths
    theta = xx[:, 4:]  # Angles

    # Compute the position on the x-coord
    xx_loc = np.zeros(len(xx))
    yy_loc = np.zeros(len(xx))

    # Compute the end locations
    for i in range(4):
        xx_loc += ll[:, i] * np.cos(np.sum(theta[:, : i + 1], axis=1))
        yy_loc += ll[:, i] * np.sin(np.sum(theta[:, : i + 1], axis=1))

    # Compute the distance between end location and origin
    yy = np.sqrt(xx_loc**2 + yy_loc**2)

    return yy
