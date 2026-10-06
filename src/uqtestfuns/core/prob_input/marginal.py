"""
Module with an implementation of ``Marginal`` class.

This module provides the :class:`Marginal` class, which models a single random
variable through a parametric probability distribution. It is intended as
the building block for probabilistic input models, where each input dimension
is described by one marginal distribution.

The class offers a consistent interface for:

- Validating the chosen distribution and its parameters
- Evaluating the probability density function (PDF)
- Evaluating the cumulative distribution function (CDF)
- Computing the inverse CDF (ICDF)
- Generating random samples
- Transforming samples between marginal distributions

For numerical purposes, each distribution is associated with finite lower and
upper bounds. These bounds are used when evaluating PDFs, CDFs,
and inverse CDFs through the helper functions imported from :mod:`.utils`.
"""

from __future__ import annotations

import numpy as np

from numpy.typing import ArrayLike
from typing import Optional, Union

from .utils import (
    verify_distribution,
    get_distribution_bounds,
    verify_parameters,
    get_pdf_values,
    get_cdf_values,
    get_icdf_values,
    get_display_name,
    get_parameter_names,
)

__all__ = ["Marginal"]

# Ordered field names for printing purpose
FIELD_NAMES = ["name", "distribution", "parameters", "description"]


class Marginal:
    """A random variable represented by a univariate probability distribution.

    The class represents a single random variable defined by its distribution
    type and parameters. Within a probabilistic input model, each univariate
    distribution serves as a marginal of the joint distribution.

    Parameters
    ----------
    distribution : str
        The type of probability distribution.
    parameters : array_like
        The parameters of the chosen probability distribution.
    name : str, optional
        The name of the random variable.
    description : str, optional
        A short text description of the random variable.
    """

    def __init__(
        self,
        distribution: str,
        parameters: ArrayLike,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        # Assign and verify the distribution type
        self._distribution = distribution.lower()
        verify_distribution(self.distribution)

        # Assign and verify the parameters
        self._parameters = np.array(parameters)
        verify_parameters(self.distribution, self.parameters)

        # Assign the name and description
        self._name = name
        self._description = description

        # Compute the lower and upper bounds of the distribution
        self._lower, self._upper = get_distribution_bounds(
            self.distribution,
            self.parameters,
        )

    # --- Public properties
    @property
    def distribution(self) -> str:
        """The type of the probability distribution.

        Returns
        -------
        str
            The type of the one-dimensional marginal distribution.
        """
        return self._distribution

    @property
    def parameters(self) -> np.ndarray:
        """The parameters of the chosen probability distribution.

        Returns
        -------
        np.ndarray
            The parameters of the chosen probability distribution.
        """
        return self._parameters

    @property
    def name(self) -> Optional[str]:
        """The name of the random variable.

        Returns
        -------
        str, optional
            The name of the random variable.
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """A short text description of the random variable.

        Returns
        -------
        str, optional
            A short text description of the random variable.
        """
        return self._description

    @property
    def lower(self) -> float:
        """The lower bound of the distribution.

        Returns
        -------
        float
            The lower bound of the distribution.

        Notes
        -----
        - While the support of many continuous probability density functions
          is unbounded, numerically they are always bounded. Below the lower
          bound, the density values are always zero.
        """
        return self._lower

    @property
    def upper(self) -> float:
        """The upper bound of the distribution.

        Returns
        -------
        float
            The upper bound of the distribution.

        Notes
        -----
        - While the support of many continuous probability density functions
          is unbounded, numerically they are always bounded. Above the upper
          bound, the density values are always zero.
        """
        return self._upper

    @property
    def notation(self) -> str:
        """Display the distribution formula.

        Returns
        -------
        str
            The distribution notation, e.g., "Normal(mu=0.0, sigma=1.0)".
        """
        display_name = get_display_name(self.distribution)
        param_names = get_parameter_names(self.distribution)

        items = [
            f"{name}={value:.6g}"
            for name, value in zip(param_names, self.parameters, strict=True)
        ]
        notation_ = f"{display_name}({', '.join(items)})"

        return notation_

    # --- Public methods
    def pdf(self, xx: Union[float, np.ndarray]) -> np.ndarray:
        """Compute the probability density function of the distribution.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The input values in the support of the distribution.

        Returns
        -------
        np.ndarray
            The probability density function (PDF) values at the input values.
            The output is an array of at least one dimension.
        """
        # Convert input to a NumPy array of at least one dimension
        xx = np.atleast_1d(xx)

        return get_pdf_values(
            xx,
            self.distribution,
            self.parameters,
            self.lower,
            self.upper,
        )

    def cdf(self, xx: Union[float, np.ndarray]) -> np.ndarray:
        """Compute the cumulative distribution function on input values.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The input values in the support of the distribution.

        Returns
        -------
        np.ndarray
            The cumulative distribution function (CDF) values at the input
            values. The output is an array of at least one dimension.
        """
        # Convert input to a NumPy array of at least one dimension
        xx = np.atleast_1d(xx)

        return get_cdf_values(
            xx,
            self.distribution,
            self.parameters,
            self.lower,
            self.upper,
        )

    def icdf(self, xx: Union[float, np.ndarray]) -> np.ndarray:
        """Compute the inverse CDF on input values.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The input values in the [0,1] domain.

        Returns
        -------
        np.ndarray
            The inverse cumulative distribution function (ICDF) values at the
            input points. These are points in the distribution's support.
            The output is an array of at least one dimension.

        Notes
        -----
        - If the input values are outside the [0, 1] domain, NaN values
          are returned.
        """
        # Convert input to a NumPy array of at least one dimension
        xx = np.atleast_1d(xx)

        return get_icdf_values(
            xx,
            self.distribution,
            self.parameters,
            self.lower,
            self.upper,
        )

    def get_sample(
        self,
        sample_size: int = 1,
        rng: Optional[Union[np.random.Generator, int]] = None,
    ) -> np.ndarray:
        """Get a random sample from the distribution.

        Parameters
        ----------
        sample_size : int, optional
            The number of sample points. Default is 1.
        rng :  Union[np.random.Generator, int], optional
            The random number generator or the seed for the default NumPy
            random number generator. If not specified, the default random
            number generator with the operating system entropy is used.

        Returns
        -------
        np.ndarray
            A one-dimensional array of length ``sample_size`` containing
            the sample points.
        """
        if rng is None or isinstance(rng, int):
            rng = np.random.default_rng(rng)

        # Draw random sample in [0, 1]
        xx = rng.random(sample_size)

        # Return the transformed sample in the current distribution
        return self.icdf(xx)

    def transform_to(
        self,
        xx: Union[float, np.ndarray],
        target: Marginal,
    ) -> np.ndarray:
        """Transform a sample from this distribution to another.

        Parameters
        ----------
        xx : Union[float, np.ndarray]
            The sample points to be transformed.
        target : Marginal
            The target distribution to which the sample should be transformed.

        Returns
        -------
        np.ndarray
            The transformed sample points in the target distribution.
            The output is an array of at least one dimension.
        """
        if not isinstance(target, Marginal):
            raise TypeError("Other instance must be of Marginal type!")

        # Transform the sample to [0, 1]
        xx_trans = self.cdf(xx)

        # Transform the sample in [0, 1] to the other distribution
        return target.icdf(xx_trans)

    # --- Dunder methods
    def __eq__(self, other: object) -> bool:
        """Check the equality in value between two instances.

        An equality in value between two instances of Marginal means that:

        - The distributions are the same
        - The parameters are the same
        - The name and description are the same

        Parameters
        ----------
        other : object
            The other instance to compare with.

        Returns
        -------
        bool
            True if the two instances are equal in value, False otherwise.
        """
        if not isinstance(other, Marginal):
            return False

        if self.distribution != other.distribution:
            return False

        if not np.array_equal(self.parameters, other.parameters):
            return False

        if self.name != other.name:
            return False

        if self.description != other.description:
            return False

        return True

    def __str__(self) -> str:
        """Return a human-readable summary of the Marginal instance.

        Returns
        -------
        str
            The human-readable summary of the instance.
        """
        name = self.name
        if name is None:
            return self.notation

        return f"{name} ~ {self.notation}"

    def __repr__(self) -> str:
        """Return the unambiguous string representation of the instance.

        Returns
        -------
        str
            The unambiguous string representation of the instance.
        """
        class_name = self.__class__.__name__
        # Get the value of the constructor arguments
        attrs = {
            "distribution": self.distribution,
            "parameters": self.parameters.tolist(),
            "name": self.name,
            "description": self.description,
        }
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())

        return f"{class_name}({attrs_str})"
