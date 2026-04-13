"""
This is the conftest module for UQTestFuns.

All global fixtures are defined here.
"""

import numpy as np
import string
from typing import List, Callable, Any, Dict

from uqtestfuns.core.prob_input.utils import SUPPORTED_MARGINALS
from uqtestfuns.core.prob_input.marginal import Marginal

MARGINALS = list(SUPPORTED_MARGINALS.keys())


def create_random_alphanumeric(length: int, rng=None) -> str:
    """Create a random alphanumeric string of a given length.

    Parameters
    ----------
    length : int
        Length of the string
    rng : Union[np.random.Generator, int], optional
        The random number generator or the seed for the default NumPy

    Returns
    -------
    str
        A random alphanumeric string of the given length.
    """
    if rng is None or isinstance(rng, int):
        rng = np.random.default_rng(rng)

    out = "".join(
        rng.choice(list(string.ascii_letters + string.digits), size=length)
    )

    return out


def create_random_marginal_dicts(
    length: int,
    rng=None,
) -> List[Dict]:
    """Create a random list of univariate random variables.

    Parameters
    ----------
    length : int
        Length of the list of dictionaries.
    rng : Union[np.random.Generator, int], optional
        The random number generator or the seed for the default NumPy
    Returns
    -------
    List[Marginal]
        List of dictionaries to specify a ProbInput instance.
    """
    if rng is None or isinstance(rng, int):
        rng = np.random.default_rng(rng)

    marginals = []

    for i in range(length):
        distribution = rng.choice(MARGINALS)
        if distribution == "beta":
            parameters = np.sort(1 + 2 * rng.random(4))
        elif distribution == "exponential":
            # Single parameter, must be strictly positive
            parameters = 1 + rng.random(1)
        elif distribution == "triangular":
            parameters = np.sort(1 + 2 * rng.random(2))
            parameters = np.insert(
                parameters, 2, rng.uniform(parameters[0], parameters[1])
            )
        elif distribution in ["trunc-normal", "trunc-gumbel"]:
            # mu must be inside the bounds
            parameters = np.sort(1 + 2 * rng.random(3))
            parameters[[0, 1]] = parameters[[1, 0]]
            # Insert sigma/beta as the second parameter
            parameters = np.insert(parameters, 1, 0.5 + rng.random(1))
        elif distribution == "lognormal":
            # Limit the size of the parameters
            parameters = 1 + rng.random(2)
        else:
            parameters = np.sort(1 + 2 * rng.random(2))

        marginals.append(
            {
                "name": f"X{i+1}",
                "distribution": distribution,
                "parameters": parameters,
                "description": create_random_alphanumeric(10, rng),
            }
        )

    return marginals


def create_random_marginals(length: int) -> List[Marginal]:
    """Create a random list of univariate random variables.

    Parameters
    ----------
    length : int
        Length of the list of dictionaries.

    Returns
    -------
    List[Marginal]
        List of dictionaries to specify a ProbInput instance.
    """
    marginal_dicts = create_random_marginal_dicts(length)

    return [Marginal(**marginal_dict) for marginal_dict in marginal_dicts]


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
