"""
Module with an implementation of MultivariateInput class.

The MultivariateInput class represents a multivariate probabilistic input.
Each multivariate input has a set of marginals defined by an instance of
the UnivariateInput class.
"""
import numpy as np
from dataclasses import dataclass, InitVar, field
from typing import List, Dict, Any

from .univariate_input import UnivariateInput


__all__ = ["MultivariateInput"]


@dataclass
class MultivariateInput:
    """A class for multivariate input variables.

    Attributes
    ----------
    spatial_dimension : int
        Number of univariate inputs.
    marginals : List[UnivariateInput]
        List of marginals of univariate inputs.
    copulas : Any
        Copulas between univariate inputs that define dependence structure
        (currently not used).

    Parameters
    ----------
    univariate_inputs : List[Dict]
        List of dictionaries that defines each of the univariate inputs.
    """
    spatial_dimension: int = field(init=False)
    marginals: List[UnivariateInput] = field(init=False)
    univariate_inputs: InitVar[List[Dict]] = None
    copulas: Any = None

    def __post_init__(self, univariate_inputs: List[Dict]):
        self.spatial_dimension = len(univariate_inputs)
        self.marginals = []
        for univariate_input in univariate_inputs:
            self.marginals.append(UnivariateInput(**univariate_input))

    def transform_sample(self, other, xx: np.ndarray):
        """Transform a sample from the distribution to another."""
        # Make sure the dimensionality is consistent
        if self.spatial_dimension != other.spatial_dimension:
            raise ValueError(
                "The dimensionality of the two inputs are not consistent!"
            )

        xx_trans = xx.copy()
        if self.copulas is None:
            # Independent inputs, transform marginal by marginal
            for idx_dim, (marginal_self, marginal_other) in \
                    enumerate(zip(self.marginals, other.marginals)):
                xx_trans[:, idx_dim] = marginal_self.transform_sample(
                    marginal_other, xx[:, idx_dim]
                )
        else:
            raise ValueError("Copulas are not currently supported!")

        return xx_trans

    def get_sample(self, sample_size: int = 1):
        """Get a random sample from the distribution."""
        # Create an instance univariate sample
        univ_input = UnivariateInput(
            name="X", distribution="uniform", parameters=[0, 1]
        )

        xx = np.random.rand(sample_size, self.spatial_dimension)
        # Transform the sample in [0, 1] to the domain of the distribution
        if self.copulas is None:
            # Independent inputs generate sample marginal by marginal
            for idx_dim, marginal in enumerate(self.marginals):
                xx[:, idx_dim] = univ_input.transform_sample(
                    marginal, xx[:, idx_dim]
                )
        else:
            raise ValueError("Copulas are not currently supported!")

        return xx

    def pdf(self, xx: np.ndarray) -> np.ndarray:
        """Get the PDF value of the distribution on a set of values.

        Parameters
        ----------
        xx : np.ndarray
            Sample values (realizations) from a distribution.

        Returns
        -------
        np.ndarray
            PDF values of the distribution on the sample values.
        """
        if self.copulas is None:
            yy = np.empty(xx.shape)
            for i, marginal in enumerate(self.marginals):
                yy[:, i] = marginal.pdf(xx[:, i])
            # Use log-transform because of the smallness of numbers
            yy = np.exp(np.sum(np.log(yy), axis=1))
        else:
            raise ValueError("Copulas are not currently supported!")

        return yy
