"""
Utility module for univariate distribution calculations.
"""
import numpy as np

from ....global_settings import ARRAY_FLOAT


def postprocess_icdf(
    xx: ARRAY_FLOAT,
    lower_bound: float,
    upper_bound: float,
) -> ARRAY_FLOAT:
    """Postprocess the computed ICDF values.

    The postprocessing ensures that the output is an array and always
    within the bounds of the distribution and

    Parameters
    ----------
    xx : ARRAY_FLOAT
        The raw ICDF values of a distribution computed either from a built-in
        function or a re-parameterization of the SciPy implementation.
    lower_bound : float
        The lower bound of the distribution. All values below this value will
        automatically be set to this value.
    upper_bound : float
        The upper bound of the distribution. All values above this value will
        automatically be set to this value.

    Return
    ------
    ARRAY_FLOAT
        The post-processed ICDF values.
    """
    # A scalar output
    if xx.ndim == 0:
        if xx < lower_bound:
            xx = lower_bound
        if xx > upper_bound:
            xx = upper_bound

        xx = np.asarray(xx)

    else:
        xx[xx < lower_bound] = lower_bound
        xx[xx > upper_bound] = upper_bound

    return xx
