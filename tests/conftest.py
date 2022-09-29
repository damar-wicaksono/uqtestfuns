"""
This is the conftest module for UQTestFuns.

All global fixtures are defined here.
"""
import numpy as np
import random
import string
from typing import List, Dict

from uqtestfuns.core.prob_input.utils import SUPPORTED_MARGINALS

MARGINALS = list(SUPPORTED_MARGINALS.keys())


def create_random_alphanumeric(length: int) -> str:
    """Create a random alphanumeric string of a given length.

    Parameters
    ----------
    length : int
        Length of the string

    Returns
    -------
    str
        A random alphanumeric string of the given length.
    """

    out = "".join(
        random.choice(string.ascii_letters+string.digits) for _ in range(length)
    )

    return out


def create_random_input_dicts(length: int) -> List[Dict]:
    """Create a random multivariate input dictionaries.

    Parameters
    ----------
    length : int
        Length of the list of dictionaries.

    Returns
    -------
    List[Dict]
        List of dictionaries to specify a MultivariateInput class.
    """
    input_dicts = []

    for i in range(length):
        distribution = random.choice(MARGINALS)
        if distribution == "beta":
            parameters = np.sort(1 + 2 * np.random.rand(4))
        else:
            parameters = np.sort(1 + 2 * np.random.rand(2))
        input_dicts.append(
            {
                "name": f"X{i+1}",
                "distribution": distribution,
                "parameters": parameters,
                "description": create_random_alphanumeric(10)
             }
        )

    return input_dicts


def assert_call(fct, *args, **kwargs):
    """Assert that a call runs as expected."""
    try:
        fct(*args, **kwargs)
    except Exception as e:
        print(type(e))
        raise AssertionError(
            f"The function was not called properly. "
            f"It raised the exception:\n\n {e.__class__.__name__}: {e}"
        )

