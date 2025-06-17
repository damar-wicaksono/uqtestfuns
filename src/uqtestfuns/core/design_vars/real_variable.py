"""
Module with concrete implementation of real (continuous) design variables.
"""

from __future__ import annotations

import numpy as np

from numpy.random._generator import Generator
from typing import Optional, Union

from .design_variable_abc import DesignVariableABC


class RealVariable(DesignVariableABC):
    """Class representing a real (continuous) bounded design variable.

    Parameters
    ----------
    lower : float
        The lower bound of the continuous design variable.
    upper : float
        The upper bound of the continuous design variable.
    name : str, optional
        The name of the design variable. If not specified, the value is None.
    description : str, optional
        The short description of the design variable. If not specified,
        the value is None.
    rng_seed : int, optional
        The seed number to initialize an internal random number generator.
    """

    def __init__(
        self,
        lower: float,
        upper: float,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rng_seed: Optional[int] = None,
    ) -> None:

        _verify_bounds(lower, upper)
        self._lower = float(lower)
        self._upper = float(upper)
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self._rng_seed = rng_seed
        self._rng: Optional[Generator] = None

    @property
    def bounds(self) -> tuple[float, float]:
        return self._lower, self._upper

    @property
    def rng(self) -> Generator:
        if self._rng is None:
            self._rng = np.random.default_rng(self._rng_seed)
        return self._rng

    @property
    def rng_seed(self) -> Optional[int]:
        return self._rng_seed

    @rng_seed.setter
    def rng_seed(self, value: Optional[int]):
        self.reset_rng(value)

    def get_sample(self, sample_size: int) -> np.ndarray:
        """Get a random sample of design variable values.

        Parameters
        ----------
        sample_size : int
            The number of sample points to generate.

        Returns
        -------
        np.ndarray
            The generated sample in an array of length :math:`N`.
        """
        lower, upper = self.bounds
        xx = self.rng.uniform(lower, upper, size=sample_size)

        return xx

    def is_valid(
        self,
        xx: Union[float, np.ndarray],
    ) -> Union[bool, np.ndarray]:
        """Check if the given value is valid.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The value to be checked; it can be a scalar or an array.
        """
        return np.logical_and(xx >= self._lower, xx <= self._upper)

    def transform_to(
        self,
        xx: Union[float, np.ndarray],
        lower: float,
        upper: float,
    ) -> Union[float, np.ndarray]:
        """Transform sample values from specified bounds to target bounds.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The sample values to be transformed.
        lower : float
            The lower target bound.
        upper : float
            The upper target bound.

        Returns
        -------
        Union[float, np.ndarray]
            The transformed sample values.
        """
        _verify_bounds(lower, upper)
        if not np.all(self.is_valid(xx)):
            raise ValueError("The given sample is not valid!")

        origin_lower, origin_upper = self.bounds
        origin_diff = origin_upper - origin_lower

        return lower + (upper - lower) / origin_diff * (xx - origin_lower)

    def transform_from(
        self,
        xx: Union[float, np.ndarray],
        lower: float,
        upper: float,
    ) -> Union[float, np.ndarray]:
        """Transform sample values from a set of origin bounds.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The sample values to be transformed.
        lower : float
            The lower origin bound.
        upper : float
            The upper origin bound.

        Returns
        -------
        Union[float, np.ndarray]
            The transformed sample values.
        """
        _verify_bounds(lower, upper)
        var_temp = RealVariable(lower, upper)
        if not np.all(var_temp.is_valid(xx)):
            raise ValueError("The given sample is not valid!")

        target_lower, target_upper = self.bounds
        target_diff = target_upper - target_lower

        return target_lower + target_diff / (upper - lower) * (xx - lower)

    def __repr__(self):
        """Return the unambiguous string representation of the instance."""
        class_name = self.__class__.__name__
        # Get the value of the constructor arguments
        attrs = {
            "lower": self._lower,
            "upper": self._upper,
            "name": self.name,
            "description": self.description,
            "rng_seed": self._rng_seed,
        }
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())

        return f"{class_name}({attrs_str})"

    def __str__(self):
        """Return human-readable string representation of the instance."""
        table = "Continuous Design Variable\n"
        table += f"Lower Bound : {self._lower}\n"
        table += f"Upper Bound : {self._upper}\n"
        table += f"Name        : {self.name}\n"

        # Parse the description column
        if self.description is None or self.description == "":
            description = "-"
        else:
            description = self.description
        table += f"Description : {description}"

        return table


def _verify_bounds(lower: float, upper: float):
    """Verify if the given bounds are valid.

    Parameters
    ----------
    lower : float
        The lower bound.
    upper : float
        The upper bound.

    Raises
    ------
    ValueError
        If the lower bound is greater than or equal to the upper bound.
    """
    if lower >= upper:
        raise ValueError("Lower bound must be smaller than upper bound.")
