"""
Module with an implementation of the 2D cantilever beam reliability problem.

The 2D cantilever beam problem is a reliability test function from [1].
This is an often revisited problem in reliability analysis ([2], [3]).

The problem consists of a cantilever beam with a rectangular cross-section
subjected to a uniformly distributed loading. The maximum deflection
at the free end is taken to be the performance criterion.


References
----------
1. Malur R. Rajashekhar and Bruce R. Ellingwood, “A new look at the response
   surface approach for reliability analysis,” Structural Safety,
   vol. 12, no. 3, pp. 205–220, 1993.
   DOI: 10.1016/0167-4730(93)90003-J
2. Luc Schueremans and Dionys Van Gemert, “Benefit of splines and neural
   networks in simulation based structural reliability analysis,” Structural
   Safety, vol. 27, no. 3, pp. 246–261, 2005.
   DOI: 10.1016/j.strusafe.2004.11.001
3. X. Li, C. Gong, L. Gu, W. Gao, Z. Jing, and H. Su, “A sequential surrogate
   method for reliability analysis based on radial basis function,”
   Structural Safety, vol. 73, pp. 42–53, 2018.
   DOI: 10.1016/j.strusafe.2018.02.005
"""

import numpy as np


def evaluate(xx: np.ndarray, modulus: float, span: float) -> np.ndarray:
    """Evaluate the 2D cantilever beam function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        A two-dimensional input values given by an N-by-2 array
        where N is the number of input values.
    modulus : float
        The modulus of elasticity in [MPa].
    span : float
        The span of the beam in [mm].

    Returns
    -------
    np.ndarray
        The performance function (serviceability) of the cantilever beam
        system. If negative, the system is in failed state.
        The output is a one-dimensional array of length N.
    """
    # Convert modulus from [MPa] to [N/mm^2] to match the unit of W [N/m^2]
    # after accounting for the mm^4/mm^3 = mm terms from span and depth
    modulus *= 1e6  # from [MPa] to [Pa]

    # Get the input
    ww = xx[:, 0]  # Load per unit area [N/m^2] ([Pa])
    hh = xx[:, 1]  # Depth of the cross-section [mm]

    # Compute the performance function
    yy = span / 325 - 12 / 8 * span**4 / modulus * ww / hh**3

    return yy
