"""
This is the conftest module for UQTestFuns.

All global fixtures are defined here.
"""
import numpy as np
import random
import string
from typing import List, Callable, Any

from uqtestfuns.core.prob_input.utils import SUPPORTED_MARGINALS
from uqtestfuns.core.prob_input.univariate_distribution import UnivDist

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
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )

    return out


def create_random_marginals(length: int) -> List[UnivDist]:
    """Create a random list of univariate random variables.

    Parameters
    ----------
    length : int
        Length of the list of dictionaries.

    Returns
    -------
    List[UnivDist]
        List of dictionaries to specify a ProbInput instance.
    """
    marginals = []

    for i in range(length):
        distribution = random.choice(MARGINALS)
        if distribution == "beta":
            parameters = np.sort(1 + 2 * np.random.rand(4))
        elif distribution == "exponential":
            # Single parameter, must be strictly positive
            parameters = 1 + np.random.rand(1)
        elif distribution == "triangular":
            parameters = np.sort(1 + 2 * np.random.rand(2))
            parameters = np.insert(
                parameters, 2, np.random.uniform(parameters[0], parameters[1])
            )
        elif distribution in ["trunc-normal", "trunc-gumbel"]:
            # mu must be inside the bounds
            parameters = np.sort(1 + 2 * np.random.rand(3))
            parameters[[0, 1]] = parameters[[1, 0]]
            # Insert sigma/beta as the second parameter
            parameters = np.insert(parameters, 1, np.random.rand(1))
        elif distribution == "lognormal":
            # Limit the size of the parameters
            parameters = 1 + np.random.rand(2)
        else:
            parameters = np.sort(1 + 2 * np.random.rand(2))

        marginals.append(
            UnivDist(
                name=f"X{i+1}",
                distribution=distribution,
                parameters=parameters,
                description=create_random_alphanumeric(10),
            )
        )

    return marginals


def assert_call(fct: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    """Assert that a call runs as expected."""
    try:
        fct(*args, **kwargs)
    except Exception as e:
        print(type(e))
        raise AssertionError(
            f"The function was not called properly. "
            f"It raised the exception:\n\n {e.__class__.__name__}: {e}"
        )
