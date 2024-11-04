"""
Module with an implementation of ``ProbInput`` class.

The ``ProbInput`` class represents a probabilistic input model.
Each probabilistic input has a set of one-dimensional marginals each of which
is defined by an instance of the ``UnivDist`` class.
"""

from __future__ import annotations

import numpy as np
import textwrap

from dataclasses import dataclass, field
from numpy.random._generator import Generator
from tabulate import tabulate
from typing import Any, List, Optional, Union, Tuple

from .univariate_distribution import UnivDist, FIELD_NAMES
from .input_spec import ProbInputSpecFixDim, ProbInputSpecVarDim

__all__ = ["ProbInput"]


@dataclass
class ProbInput:
    """A class for multivariate input variables.

    Parameters
    ----------
    marginals : Union[List[UnivDist], Tuple[UnivDist, ...]]
        A list of one-dimensional marginals (univariate random variables).
    copulas : Any
        Copulas between univariate inputs that define dependence structure
        (currently not used).
    name : str, optional
        The name of the probabilistic input model.
    description : str, optional
        The short description regarding the input model.
    rng_seed : int, optional.
        The seed used to initialize the pseudo-random number generator.
        If not specified, the value is taken from the system entropy.

    Attributes
    ----------
    input_dimension : int
        Number of constituents (random) input variables.
    _rng : Generator
        The default pseudo-random number generator of NumPy.
        The generator is only created if or when needed (e.g., generating
        a random sample from the distribution).
    """

    input_dimension: int = field(init=False)
    marginals: Union[List[UnivDist], Tuple[UnivDist, ...]]
    copulas: Any = None
    name: Optional[str] = None
    description: Optional[str] = None
    rng_seed: Optional[int] = field(default=None, repr=False)
    _rng: Optional[Generator] = field(init=False, default=None, repr=False)

    def __post_init__(self):
        self.input_dimension = len(self.marginals)
        # Protect marginals by making it immutable
        self.marginals = tuple(self.marginals)

    def transform_sample(self, xx: np.ndarray, other: ProbInput):
        """Transform a sample from the distribution to another."""
        # Make sure the dimensionality is consistent
        if self.input_dimension != other.input_dimension:
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
            and the number of input dimensions, respectively.
        """
        if self._rng is None:  # pragma: no cover
            # Create a pseudo-random number generator (lazy evaluation)
            self._rng = np.random.default_rng(self.rng_seed)

        xx = self._rng.random((sample_size, self.input_dimension))
        if not self.copulas:
            # Transform the sample in [0, 1] to the domain of the distribution
            for idx_dim, marginal in enumerate(self.marginals):
                xx[:, idx_dim] = marginal.icdf(xx[:, idx_dim])
        else:
            raise ValueError("Copulas are not currently supported!")

        return xx

    def reset_rng(self, rng_seed: Optional[int]) -> None:
        """Reset the random number generator.

        Parameters
        ----------
        rng_seed : int, optional.
            The seed used to initialize the pseudo-random number generator.
            If not specified, the value is taken from the system entropy.
        """
        rng = np.random.default_rng(rng_seed)
        object.__setattr__(self, "_rng", rng)
        object.__setattr__(self, "rng_seed", rng_seed)

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
        table = f"Name            : {self.name}\n"
        table += f"Input Dimension : {self.input_dimension}\n"

        # Parse the description column
        if self.description is None or self.description == "":
            description = "-"
        else:
            desc = textwrap.wrap(self.description, width=57)
            # Pad new lines
            if len(desc) > 1:
                desc[1:] = ["                  " + line for line in desc[1:]]
            description = "\n".join(desc)
        table += f"Description     : {description}\n"
        table += "Marginals       :\n\n"

        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(self.marginals, FIELD_NAMES)

        table += tabulate(
            list_values,
            headers=header_names,
            stralign="center",
            disable_numparse=True,
        )

        table += f"\n\nCopulas         : {self.copulas}"

        return table

    @classmethod
    def from_spec(
        cls,
        prob_input_spec: Union[ProbInputSpecFixDim, ProbInputSpecVarDim],
        *,
        input_dimension: Optional[int] = None,
        rng_seed: Optional[int] = None,
    ):
        """Create an instance from a ProbInputSpec instance."""

        if isinstance(prob_input_spec, ProbInputSpecVarDim):
            if input_dimension is None:
                raise ValueError("Input dimension must be specified!")
            marginals_gen = prob_input_spec.marginals_generator
            marginals_spec = marginals_gen(input_dimension)
        else:
            marginals_spec = prob_input_spec.marginals

        # Create a list of UnivDist instances representing univariate marginals
        marginals = [
            UnivDist.from_spec(marginal) for marginal in marginals_spec
        ]

        return cls(
            marginals=marginals,
            copulas=prob_input_spec.copulas,
            name=prob_input_spec.name,
            description=prob_input_spec.description,
            rng_seed=rng_seed,
        )


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
            attr_value = getattr(marginal, field_name)
            if attr_value is None:
                attr_value = "-"
            values.append(attr_value)
        list_values.append(values)

    return list_values
