"""
Module with an implementation of ``ProbInput`` class.

The ``ProbInput`` class represents a probabilistic input model.
Each probabilistic input has a set of one-dimensional marginals each of which
is defined by an instance of the ``Marginal`` class.
"""

from __future__ import annotations

import numpy as np
import textwrap

from numpy.random._generator import Generator
from tabulate import tabulate
from typing import Any, List, Optional, Sequence

from .marginal import Marginal, FIELD_NAMES

__all__ = ["ProbInput"]


class ProbInput:
    """A class for multivariate input variables.

    Parameters
    ----------
    marginals : Union[List[Marginal], Tuple[Marginal, ...]]
        A list of one-dimensional marginals (univariate random variables).
    copulas : Any
        Copulas between univariate inputs that define dependence structure
        (currently not used).
    input_id: str, optional
        The ID of the probabilistic input. If not specified, the value is None.
    function_id: str, optional
        The ID of the function associated with the input. If not specified,
        the value is None.
    description: str, optional
        The short description regarding the input model.
    rng_seed : int, optional.
        The seed used to initialize the pseudo-random number generator.
        If not specified, the value is taken from the system entropy.
    """

    def __init__(
        self,
        marginals: Sequence[Marginal],
        copulas: Any = None,
        input_id: Optional[str] = None,
        function_id: Optional[str] = None,
        description: Optional[str] = None,
        rng_seed: Optional[int] = None,
    ):
        # Read-only properties
        self._marginals = marginals
        self._copulas = copulas
        # Attributes
        self.input_id = input_id
        self.function_id = function_id
        self.description = description
        # Other properties
        self._rng_seed = rng_seed
        self._rng: Optional[Generator] = None

    @property
    def input_dimension(self) -> int:
        """Return the number of constituents (random) input variables."""
        return len(self._marginals)

    @property
    def marginals(self) -> Sequence[Marginal]:
        """Return the sequence of Marginals that define the input variables."""
        return self._marginals

    @property
    def copulas(self) -> Any:
        """Return the underlying Copulas of the probabilistic input."""
        return self._copulas

    @property
    def rng_seed(self) -> Optional[int]:
        """Return the seed for RNG."""
        return self._rng_seed

    @rng_seed.setter
    def rng_seed(self, value: Optional[int]):
        """Set/reset the seed for RNG."""
        self.reset_rng(value)

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

    def reset_rng(self, rng_seed: Optional[int]) -> None:
        """Reset the random number generator.

        Parameters
        ----------
        rng_seed : int, optional.
            The seed used to initialize the pseudo-random number generator.
            If not specified, the value is taken from the system entropy.
        """
        rng = np.random.default_rng(rng_seed)
        self._rng = rng
        self._rng_seed = rng_seed

    def __str__(self):
        """Return human-readable string representation of the instance."""
        if self.input_id is None or self.input_id == "":
            input_id = "-"
        else:
            input_id = self.input_id
        if self.function_id is None or self.function_id == "":
            function_id = "-"
        else:
            function_id = self.function_id
        table = f"Function ID     : {function_id}\n"
        table += f"Input ID        : {input_id}\n"
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

        if self.input_dimension == 1:
            return table

        # Temporary solution for independence copula
        copulas = "Independence" if self.copulas is None else self.copulas

        table += f"\n\nCopulas         : {copulas}"

        return table

    def __repr__(self):
        """Return the unambiguous string representation of the instance."""
        class_name = self.__class__.__name__
        # Get the value of the constructor arguments
        attrs = {
            "marginals": self.marginals,
            "copulas": self.copulas,
            "input_id": self.input_id,
            "function_id": self.function_id,
            "description": self.description,
            "rng_seed": self.rng_seed,
        }
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())

        return f"{class_name}({attrs_str})"


def _get_values_as_list(
    univ_inputs: Sequence[Marginal],
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
