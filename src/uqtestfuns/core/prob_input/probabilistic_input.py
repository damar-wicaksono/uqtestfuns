"""
Module with an implementation of ``ProbInput`` class.

The ``ProbInput`` class represents a probabilistic input model.
Each probabilistic input has a set of one-dimensional marginals each of which
is defined by an instance of the ``UnivDist`` class.
"""
from __future__ import annotations

import numpy as np
from tabulate import tabulate
from typing import Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field

from .univariate_distribution import UnivDist, FIELD_NAMES


__all__ = ["ProbInput"]


@dataclass
class ProbInput:
    """A class for multivariate input variables.

    Parameters
    ----------
    marginals : Union[List[UnivDist], Tuple[UnivDist, ...]]
        A list of one-dimensional marginals (univariate random variables)
    copulas : Any
        Copulas between univariate inputs that define dependence structure
        (currently not used)
    name : str, optional
        The name of the probabilistic input model
    description : str, optional
        The short description regarding the input model

    Attributes
    ----------
    spatial_dimension : int
        Number of constituents (random) input variables.
    """

    spatial_dimension: int = field(init=False)
    marginals: Union[List[UnivDist], Tuple[UnivDist, ...]]
    copulas: Any = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        self.spatial_dimension = len(self.marginals)
        # Protect marginals by making it immutable
        self.marginals = tuple(self.marginals)

    def transform_sample(self, xx: np.ndarray, other: ProbInput):
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

    def get_sample(self, sample_size: int = 1) -> np.ndarray:
        """Get a random sample from the distribution.

        Parameters
        ----------
        sample_size : int
            The number of sample points in the generated sample.

        Returns
        -------
        np.ndarray
            The generated sample in an :math:`N`-by-:math:`M` array
            where :math:`N` and :math:`M` are the sample size
            and the number of spatial dimensions, respectively.
        """

        xx = np.empty((sample_size, self.spatial_dimension))
        # Transform the sample in [0, 1] to the domain of the distribution
        if not self.copulas:
            # Independent inputs generate sample marginal by marginal
            for idx_dim, marginal in enumerate(self.marginals):
                xx[:, idx_dim] = marginal.get_sample(sample_size)
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
        table = f"Name         : {self.name}\n"
        table += f"Spatial Dim. : {self.spatial_dimension}\n"
        table += f"Description  : {self.description}\n"
        table += "Marginals    :\n\n"

        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(self.marginals, FIELD_NAMES)

        table += tabulate(list_values, headers=header_names, stralign="center")

        table += f"\n\nCopulas      : {self.copulas}"

        return table

    def _repr_html_(self):
        table = f"<p><b>Name</b>:&nbsp;{self.name}\n</p>"
        table += (
            f"<p><b>Spatial Dimension</b>:&nbsp;{self.spatial_dimension}\n</p>"
        )
        table += f"<p><b>Description</b>:&nbsp;{self.description}\n</p>"
        table += "<p><b>Marginals:</b>\n</p>"

        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(self.marginals, FIELD_NAMES)

        table += tabulate(
            list_values,
            headers=header_names,
            stralign="center",
            tablefmt="html",
        )

        table += "\n"
        table += f"<p><b>Copulas</b>:&nbsp;{self.copulas}</p>"

        return table


def _get_values_as_list(
    univ_inputs: Union[List[UnivDist], Tuple[UnivDist, ...]],
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
