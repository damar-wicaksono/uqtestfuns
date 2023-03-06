"""
Module with an implementation of the ``UnivDist`` class.

The ``UnivDist`` class represents a univariate random variable.
Each random variable has a (parametric) probability distribution.
"""
from __future__ import annotations

import numpy as np

from numpy.typing import ArrayLike
from dataclasses import dataclass, field
from typing import Optional, Union

from .utils import (
    verify_distribution,
    get_distribution_bounds,
    verify_parameters,
    get_pdf_values,
    get_cdf_values,
    get_icdf_values,
)
from ...global_settings import ARRAY_FLOAT

__all__ = ["UnivDist"]

# Ordered field names for printing purpose
FIELD_NAMES = ["name", "distribution", "parameters", "description"]


@dataclass(frozen=True)
class UnivDist:
    """A class for univariate random variables.

    Parameters
    ----------
    distribution : str
        The type of the probability distribution
    parameters : ArrayLike
        The parameters of the chosen probability distribution
    name : str, optional
        The name of the random variable
    description : str, optional
        The short text description of the random variable

    Attributes
    ----------
    lower : float
        The lower bound of the distribution
    upper : float
        The upper bound of the distribution
    """

    distribution: str
    parameters: ArrayLike
    name: Optional[str] = None
    description: Optional[str] = None
    lower: float = field(init=False, repr=False)
    upper: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Because frozen=True, post init must access self via setattr
        # Make sure the distribution is lower-case
        object.__setattr__(self, "distribution", self.distribution.lower())

        # Convert parameters to a numpy array
        object.__setattr__(self, "parameters", np.array(self.parameters))

        # Verify the selected univariate distribution type
        verify_distribution(self.distribution)

        # Verify the value of the parameters
        verify_parameters(self.distribution, self.parameters)

        # Get and set the lower and upper bounds
        _lower, _upper = get_distribution_bounds(
            self.distribution, self.parameters
        )
        object.__setattr__(self, "lower", _lower)
        object.__setattr__(self, "upper", _upper)

    def transform_sample(
        self,
        xx: Union[float, np.ndarray],
        other: UnivDist,
    ) -> np.ndarray:
        """Transform a sample from a given distribution to another."""
        if not isinstance(other, UnivDist):
            raise TypeError("Other instance must be of UnivariateType!")

        xx_trans = self.cdf(xx)

        return get_icdf_values(
            xx_trans,
            other.distribution,
            other.parameters,
            other.lower,
            other.upper,
        )

    def get_sample(self, sample_size: int = 1) -> np.ndarray:
        """Get a random sample from the distribution."""
        xx = np.random.rand(sample_size)

        return get_icdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )

    def pdf(self, xx: Union[float, np.ndarray]) -> ARRAY_FLOAT:
        """Compute the PDF of the distribution on a set of values."""
        # TODO: check if you put a scalar inside
        # Convert input to an np.array
        xx = np.asarray(xx)

        return get_pdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )

    def cdf(self, xx: Union[float, np.ndarray]) -> ARRAY_FLOAT:
        """Compute the CDF of the distribution on a set of values.

        The function transforms the sample values in the domain
        of the distribution to the [0, 1] domain.
        """
        # TODO: check if you put a scalar inside
        # Convert input to an np.array
        xx = np.asarray(xx)

        return get_cdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )

    def icdf(self, xx: Union[float, np.ndarray]) -> ARRAY_FLOAT:
        """Compute the inverse CDF of the distribution on a set of values.

        The function transforms values in the [0,1] domain to the domain
        of the distribution.
        """
        # TODO: verify that the input is in [0, 1]
        xx = np.asarray(xx)

        return get_icdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )
