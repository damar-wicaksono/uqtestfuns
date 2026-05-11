"""
Module with an implementation of the Piston simulation test function.

The Piston simulation test function is a seven-dimensional scalar-valued
test function.
The function computes the cycle time of a piston.
The function has been used as a test function in metamodeling exercises [1].
A 20-dimensional variant was used for sensitivity analysis in [2]
by introducing 13 additional inert input variables.

References
----------

1. E. N. Ben-Ari and D. M. Steinberg, "Modeling data from computer
   experiments: An empirical comparison of Kriging with MARS
   and projection pursuit regression," Quality Engineering,
   vol. 19, pp. 327-338, 2007.
   DOI: 10.1080/08982110701580930
2. H. Moon, "Design and Analysis of Computer Experiments for Screening Input
   Variables," Ph. D. dissertation, Ohio State University, Ohio, 2010.
   URL: http://rave.ohiolink.edu/etdc/view?acc_num=osu1275422248
"""

import numpy as np


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the Piston simulation test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        (At least) 7-dimensional input values given by N-by-M arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Piston simulation test function,
        The output is a one-dimensional array of length N.

    Notes
    -----
    - The variant of this test function has 13 additional inputs,
      but they are all taken to be inert and therefore should not affect
      the output.
    """
    mm = xx[:, 0]  # piston weight
    ss = xx[:, 1]  # piston surface area
    vv_0 = xx[:, 2]  # initial gas volume
    kk = xx[:, 3]  # spring coefficient
    pp_0 = xx[:, 4]  # atmospheric pressure
    tt_a = xx[:, 5]  # ambient temperature
    tt_0 = xx[:, 6]  # filling gas temperature

    # Compute the force
    aa = pp_0 * ss + 19.62 * mm - kk * vv_0 / ss

    # Compute the force difference
    daa = np.sqrt(aa**2 + 4.0 * kk * pp_0 * vv_0 * tt_a / tt_0) - aa

    # Compute the volume difference
    vv = ss / 2.0 / kk * daa

    # Compute the cycle time
    cc = (
        2.0
        * np.pi
        * np.sqrt(mm / (kk + ss**2 * pp_0 * vv_0 * tt_a / tt_0 / vv**2))
    )

    return cc
