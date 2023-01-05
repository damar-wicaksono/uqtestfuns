"""
Module with an implementation of MultivariateInput class.

The MultivariateInput class represents a multivariate probabilistic input.
Each multivariate input has a set of marginals defined by an instance of
the UnivariateInput class.
"""
from __future__ import annotations

import numpy as np
from tabulate import tabulate
from typing import List, Any, Union, Tuple
from dataclasses import dataclass, field

from .univariate_input import UnivariateInput, FIELD_NAMES


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
    """

    spatial_dimension: int = field(init=False)
    marginals: Union[List[UnivariateInput], Tuple[UnivariateInput, ...]]
    copulas: Any = None

    def __post_init__(self):
        self.spatial_dimension = len(self.marginals)
        # Protect marginals by making it immutable
        self.marginals = tuple(self.marginals)

    def transform_sample(self, xx: np.ndarray, other: MultivariateInput):
        """Transform a sample from the distribution to another."""
        # Make sure the dimensionality is consistent
        if self.spatial_dimension != other.spatial_dimension:
            raise ValueError(
                "The dimensionality of the two inputs are not consistent!"
            )

        xx_trans = xx.copy()
        if not self.copulas:
            # Independent inputs, transform marginal by marginal
            for idx_dim, (marginal_self, marginal_other) in enumerate(
                zip(self.marginals, other.marginals)
            ):
                xx_trans[:, idx_dim] = marginal_self.transform_sample(
                    xx[:, idx_dim], marginal_other
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
        if not self.copulas:
            # Independent inputs generate sample marginal by marginal
            for idx_dim, marginal in enumerate(self.marginals):
                xx[:, idx_dim] = univ_input.transform_sample(
                    xx[:, idx_dim], marginal
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
        if not self.copulas:
            yy = np.empty(xx.shape)
            for i, marginal in enumerate(self.marginals):
                yy[:, i] = marginal.pdf(xx[:, i])
            # Use log-transform because of the smallness of numbers
            yy = np.exp(np.sum(np.log(yy), axis=1))
        else:
            raise ValueError("Copulas are not currently supported!")

        return yy

    def __str__(self):
        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(self.marginals, FIELD_NAMES)

        return tabulate(list_values, headers=header_names, stralign="center")

    def _repr_html_(self):
        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(self.marginals, FIELD_NAMES)

        return tabulate(
            list_values,
            headers=header_names,
            stralign="center",
            tablefmt="html",
        )


def _get_values_as_list(
    univ_inputs: Union[List[UnivariateInput], Tuple[UnivariateInput, ...]],
    field_names: List[str],
) -> list:
    """Get the values from each field from a list of UnivariateInput

    Parameters
    ----------
    univ_inputs : Union[List[UnivariateInput], Tuple[UnivariateInput, ...]]
        A list or a tuple of UnivariateInput representing
        the marginal distribution.
    field_names : List[str]
        A list of field names from each UnivariateInput to access
        (and its value grabbed).

    Return
    ------
    list
        List of values.
    """
    list_values = []
    for i, marginal in enumerate(univ_inputs):
        values = [i + 1]
        for field_name in field_names:
            values.append(getattr(marginal, field_name))
        list_values.append(values)

    return list_values
