"""
This is the conftest module for UQTestFuns.

All global fixtures are defined here.
"""
import random
import string


def create_random_alphanumeric(length: int):
    """Create a random alphanumeric string of a given length.

    Parameters
    ----------
    length : int
        Length of the string
    """

    out = "".join(
        random.choice(string.ascii_letters+string.digits) for _ in range(length)
    )

    return out
