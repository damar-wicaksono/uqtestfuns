"""
Module with an abstract class for defining a design variable.
"""

from __future__ import annotations

import numpy as np

from abc import ABC, abstractmethod
from typing import Optional

__all__ = ["DesignVariableABC"]


class DesignVariableABC(ABC):

    _rng: Optional[np.random.Generator] = None
    _rng_seed: Optional[int] = None

    @property
    @abstractmethod
    def bounds(self):  # pragma: no cover
        """The bounds of the design variable."""
        pass

    @abstractmethod
    def is_valid(self, xx):  # pragma: no cover
        """Verify if the given value is valid."""
        pass

    @abstractmethod
    def get_sample(self, sample_size: int) -> np.ndarray:  # pragma: no cover
        """Get a random sample of design variable values.

        Parameters
        ----------
        sample_size : int
            The number of sample points to generate.

        Returns
        -------
        np.ndarray
            The generated sample in an :math:`N`-by-:math:`M` array
            where :math:`N` and :math:`M` are the sample size
            and the number of input dimensions, respectively.
        """
        pass

    @abstractmethod
    def transform_to(self, xx, lower: float, upper: float):  # pragma: no cover
        """Transform sample values from internal bounds to target bounds."""
        pass

    @abstractmethod
    def transform_from(
        self,
        xx,
        lower: float,
        upper: float,
    ):  # pragma: no cover
        """Transform sample values from a set of target bounds."""
        pass

    def reset_rng(self, rng_seed: Optional[int] = None):
        """Reset the random number generator.

        Parameters
        ----------
        rng_seed : Optional[int]
            The seed for the random number generator. If None, internal
            state is used.
        """
        rng = np.random.default_rng(rng_seed)
        self._rng = rng
        self._rng_seed = rng_seed
