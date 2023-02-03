"""
Module with an implementation of the ``UnivariateInput`` class.

The UnivariateInput class represents a univariate probabilistic input.
Each input has a probability distribution and the associated parameters.
"""
from __future__ import annotations

import numpy as np

from numpy.typing import ArrayLike
from dataclasses import dataclass, field
from typing import Optional

from .utils import (
    verify_distribution,
    get_distribution_bounds,
    verify_parameters,
    get_pdf_values,
    get_cdf_values,
    get_icdf_values,
)
from ...global_settings import ARRAY_FLOAT

__all__ = ["UnivariateInput"]

# Ordered field names for printing purpose
FIELD_NAMES = ["name", "distribution", "parameters", "description"]


@dataclass(frozen=True)
class UnivariateInput:
    """A class for univariate input variables.

    Attributes
    ----------
    name : str
        Name of the input variable.
    distribution : str
        Type of probability distribution.
    parameters : ArrayLike
        Parameters of the probability distribution.
    description : str, optional
        The text description of the input variable.
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
        xx: ArrayLike,
        other: UnivariateInput,
    ) -> ArrayLike:
        """Transform a sample from a given distribution to another."""
        if not isinstance(other, UnivariateInput):
            raise TypeError("Other instance must be of UnivariateType!")

        xx_trans = self.cdf(xx)

        return get_icdf_values(
            xx_trans,
            other.distribution,
            other.parameters,
            other.lower,
            other.upper,
        )

    def get_sample(self, sample_size: int = 1) -> ArrayLike:
        """Get a random sample from the distribution."""
        xx = np.random.rand(sample_size)

        return get_icdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )

    def pdf(self, xx: ArrayLike) -> ARRAY_FLOAT:
        """Compute the PDF of the distribution on a set of values."""
        # TODO: check if you put a scalar inside
        # Convert input to an np.array
        xx = np.asarray(xx)

        return get_pdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )

    def cdf(self, xx: ArrayLike) -> ARRAY_FLOAT:
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

    def icdf(self, xx: ArrayLike) -> ARRAY_FLOAT:
        """Compute the inverse CDF of the distribution on a set of values.

        The function transforms values in the [0,1] domain to the domain
        of the distribution.
        """
        # TODO: verify that the input is in [0, 1]
        xx = np.asarray(xx)

        return get_icdf_values(
            xx, self.distribution, self.parameters, self.lower, self.upper
        )
