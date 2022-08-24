"""
Module with an implementation of UnivariateInput class.

The UnivariateInput class represents a univariate probabilistic input.
Each input has a probability distribution and the associated parameters.
"""
import numpy as np
from dataclasses import dataclass, field
from typing import List, Union

from .utils import (
    verify_distribution,
    get_distribution_bounds,
    verify_parameters,
    get_pdf_values,
    get_cdf_values,
    get_icdf_values,
)

__all__ = ["UnivariateInput"]


@dataclass
class UnivariateInput:
    """A class for univariate input variables.

    Attributes
    ----------
    name : str
        Name of the input variable.
    distribution : str
        Type of probability distribution.
    parameters : Union[List, np.ndarray]
        Parameters of the probability distribution.
    """
    name: str
    distribution: str
    parameters: Union[List, np.ndarray]
    lower: float = field(init=False, repr=False)
    upper: float = field(init=False, repr=False)

    def __post_init__(self):

        # Make sure the distribution is lower-case
        self.distribution = self.distribution.lower()

        # Verify the selected univariate distribution type
        verify_distribution(self.distribution)

        # Verify the value of the parameters
        verify_parameters(self.distribution, self.parameters)

        # Convert parameters as list to a numpy array
        if isinstance(self.parameters, List):
            self.parameters = np.array(self.parameters)

        # Get the lower and upper bounds
        self.lower, self.upper = get_distribution_bounds(
            self.distribution, self.parameters
        )

    def transform_sample(self, other, xx: np.ndarray):
        """Transform a sample from a given distribution to another."""
        if not isinstance(other, UnivariateInput):
            raise TypeError("Other instance must be of UnivariateType!")

        xx_trans = self.cdf(xx)

        return get_icdf_values(xx_trans, other.distribution, other.parameters)

    def get_sample(self, sample_size: int = 1):
        """Get a random sample from the distribution."""
        xx = np.random.rand(sample_size)

        return get_icdf_values(xx, self.distribution, self.parameters)

    def pdf(self, xx: np.ndarray):
        """Compute the PDF of the distribution on a set of values."""
        return get_pdf_values(xx, self.distribution, self.parameters)

    def cdf(self, xx: np.ndarray):
        """Compute the CDF of the distribution on a set of values."""
        return get_cdf_values(xx, self.distribution, self.parameters)

    def icdf(self, xx: np.ndarray):
        """Compute the inverse CDF of the distribution on a set of values."""
        return get_icdf_values(xx, self.distribution, self.parameters)
