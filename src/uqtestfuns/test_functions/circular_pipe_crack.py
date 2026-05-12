"""
Module with an implementation of the circular pipe crack reliability problem.

The two-dimensional reliability problem was introduced in [1] and used,
for instance, in [2].

The system under consideration is as a circular pipe with a circumferential
through-wall crack under a bending moment.
If the value of the performance function is negative,
then the system is in failed state.

References
----------
1. A. K. Verma, S. Ajit, and D. R. Karanki, “Structural Reliability,”
   in Reliability and Safety Engineering, in Springer Series
   in Reliability Engineering. London: Springer London, 2016, pp. 257–292.
   DOI: 10.1007/978-1-4471-6269-8_8
2. X. Li, C. Gong, L. Gu, W. Gao, Z. Jing, and H. Su, “A sequential surrogate
   method for reliability analysis based on radial basis function,”
   Structural Safety, vol. 73, pp. 42–53, 2018.
   DOI: 10.1016/j.strusafe.2018.02.005
"""

import numpy as np


def evaluate(
    xx: np.ndarray,
    pipe_radius: float,
    pipe_thickness: float,
    bending_moment: float,
) -> np.ndarray:
    """Evaluate the circular pipe crack problem on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        An ``(N, 2)`` array of input values,
         where ``N`` is the number of input values.
    pipe_radius : float
        The radius of the pipe [m].
    pipe_thickness : float
        The thickness of the pipe [m].
    bending_moment : float
        The applied bending moment [MNm].

    Returns
    -------
    np.ndarray
        A one-dimensional array of length ``N``.
    """
    yy = (
        4
        * pipe_thickness
        * xx[:, 0]
        * pipe_radius**2
        * (np.cos(xx[:, 1] / 2) - 0.5 * np.sin(xx[:, 1]))
        - bending_moment
    )

    return yy
