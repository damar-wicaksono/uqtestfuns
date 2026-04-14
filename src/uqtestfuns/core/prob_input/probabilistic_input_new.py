"""
Module with an implementation of `ProbInput` class.

This module provides a `ProbInput` class for building, sampling, evaluating,
and transforming the probabilistic input model of an uncertainty quantification
test function.

Copula-based dependence is reserved for future support.
"""

from __future__ import annotations

import numpy as np

from numpy.typing import ArrayLike
from tabulate import tabulate
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from uqtestfuns.core.prob_input.marginal import FIELD_NAMES, Marginal

__all__ = ["ProbInput"]


class ProbInput:
    """A class representing a probabilistic input model to a UQ test function.

    A probabilistic input model to an uncertainty quantification test function
    is a random vector with a joint probability density function. It is
    defined by a sequence of one-dimensional marginal distributions and,
    optionally, a copula to model the dependence structure between the
    variables.

    Parameters
    ----------
    marginals : Sequence[Marginal]
        A sequence of one-dimensional marginal distributions.
    copulas : Any, optional
        Copulas to model the dependence structure between the variables.
        Currently, it is not used.
    name : str, optional
        The name of the probabilistic input model.
    """

    def __init__(
        self,
        marginals: Sequence[Marginal],
        copulas: Any = None,
        name: Optional[str] = None,
    ):
        # Read-only properties
        self._marginals = tuple(marginals)
        self._copulas = copulas
        self._name = name

    # --- Factory methods
    @classmethod
    def replicate(
        cls,
        dimension: int,
        distribution: str,
        parameters: ArrayLike,
        base_name: str = "X",
        *,
        copulas: Any = None,
        name: Optional[str] = None,
    ):
        """Create a probabilistic input model with replicated marginals.

        Parameters
        ----------
        dimension : int
            The dimension of the probabilistic input.
        distribution : str
            The type of the probability distribution.
        parameters :  array_like
            The parameters of the chose probability distribution.
        base_name : str, optional
            The base name for the random variables. Default is "X" and will
            be replicated as "X1", "X2", etc.
        copulas : Any, optional
            Copulas to model the dependence structure between the variables.
            Currently, it is not used.
        name : str, optional
            The name of the probabilistic input model.

        Returns
        -------
        ProbInput
            An instance of `ProbInput` class with replicated marginals.
        """
        marginals = []
        for i in range(1, dimension + 1):
            marginal_name = f"{base_name}{i}"
            marginal = Marginal(distribution, parameters, marginal_name)
            marginals.append(marginal)

        return cls(marginals, copulas, name)

    @classmethod
    def from_dicts(
        cls,
        marginals: Sequence[Dict[str, Any]],
        copulas: Any = None,
        name: Optional[str] = None,
    ):
        """Create a probabilistic input model from dictionaries.

        Parameters
        ----------
        marginals : Sequence[Dict[str, Any]]
            A sequence of dictionaries with the marginal specifications. Each
            element consists of the distribution type, parameters,
            name (optional), and description (optional) of the marginal.
        copulas : Any, optional
            Copulas to model the dependence structure between the variables.
            Currently, it is not used.
        name : str, optional
            The name of the probabilistic input model.

        Returns
        -------
        ProbInput
            An instance of `ProbInput` class with the specified marginals
            given as a sequence of dictionaries.
        """
        marginals_objects = tuple(
            [Marginal(**marginal) for marginal in marginals]
        )

        return cls(marginals_objects, copulas, name)

    @classmethod
    def from_factory(
        cls,
        factory_function: Callable,
        dimension: int,
        factory_kwargs: Optional[Dict[str, Any]] = None,
        *,
        copulas: Any = None,
        name: Optional[str] = None,
    ):
        """Create a probabilistic input model from a factory function.

        Parameters
        ----------
        factory_function : Callable
            The factory function that generates the marginal specifications.
            The function should take the dimension of input as the first
            positional argument and return a sequence of dictionaries.
        dimension : int
            The dimension of the probabilistic input model.
        factory_kwargs : Optional[Dict[str, Any]], optional
            Keyword arguments to pass to the factory function, by default None.
        copulas : Any, optional
            The copula specification for the probabilistic input model,
            by default None.
        name : Optional[str], optional
            The name of the probabilistic input model, by default None.

        Returns
        -------
        ProbInput
            An instance of `ProbInput` class with the marginals created by
            the factory function.
        """
        if factory_kwargs is None:
            marginals = factory_function(dimension)
        else:
            marginals = factory_function(dimension, **factory_kwargs)

        return cls.from_dicts(marginals, copulas, name)

    # --- Properties
    @property
    def marginals(self) -> Tuple[Marginal, ...]:
        """Return the sequence of Marginals defining the probabilistic input.

        Returns
        -------
        Tuple[Marginal, ...]
            The sequence of Marginals that defines the probabilistic input.
        """
        return self._marginals

    @property
    def copulas(self) -> Any:
        """Return the underlying Copulas of the probabilistic input.

        Returns
        -------
        Any
            The underlying Copulas of the probabilistic input.
        """
        return self._copulas

    @property
    def name(self) -> Optional[str]:
        """Return the name of the probabilistic input model.

        Returns
        -------
        str, optional
            The name of the probabilistic input model.
        """
        return self._name

    @property
    def dimension(self) -> int:
        """Return the number of random input variables.

        Returns
        -------
        int
            The number of random input variables.
        """
        return len(self.marginals)

    # --- Public methods
    def get_sample(
        self,
        sample_size: int = 1,
        rng: Union[np.random.Generator, int, None] = None,
    ) -> np.ndarray:
        r"""Generate a random sample from the probabilistic input model.

        Parameters
        ----------
        sample_size : int, optional
            The number of sample points to generate. The default is 1.
        rng :  Union[np.random.Generator, int, None]
            The random number generator or the seed for the default NumPy
            random number generator. If not specified, the default random
            number generator with the operating system entropy is used.

        Returns
        -------
        :class:`numpy:numpy.ndarray`
            The generated random sample from the probabilistic input model,
            a multi-dimensional array of shape :math:`(N, m)` where :math:`N`
            and :math:`m` are the number of samples and the dimension of the
            probabilistic input model, respectively.
        """
        if rng is None or isinstance(rng, int):
            rng = np.random.default_rng(rng)

        # Generate random sample of dimension 'm' in [0, 1]
        xx = rng.random((sample_size, self.dimension))

        if not self.copulas:
            # Iso-probabilistically transform the sample to the marginal
            for idx, marginal in enumerate(self.marginals):
                xx[:, idx] = marginal.icdf(xx[:, idx])
        else:
            raise ValueError("Copulas are not currently supported!")

        return xx

    def transform_to(
        self,
        xx: np.ndarray,
        target: Union[ProbInput, Tuple[float, float]] = (-1.0, 1.0),
    ) -> np.ndarray:
        """Transform a sample from this input model to another.

        Parameters
        ----------
        xx : :class:`numpy:numpy.ndarray`
            The sample points from the source (this) probabilistic input model.
        target : Union[ProbInput, Tuple[float, float]], optional
            The target probabilistic input model, or a tuple ``(lower, upper)``
            specifying the bounds of a hypercube with independent uniform
            marginals. The default is ``(-1.0, 1.0)``.

        Returns
        -------
        :class:`numpy:numpy.ndarray`
            The transformed sample from the current probabilistic input model
            to the target probabilistic input model.
        """
        target_ = self._prepare_transform(xx, target)

        if self.copulas:
            raise ValueError("Copulas are not currently supported!")

        xx_trans = np.empty(xx.shape)
        # Independence copula, transform marginal by marginal
        zipped_marginals = zip(self.marginals, target_.marginals)
        for i, (m_self, m_target) in enumerate(zipped_marginals):
            xx_trans[:, i] = m_self.transform_to(xx[:, i], m_target)

        return xx_trans

    def transform_from(
        self,
        xx: np.ndarray,
        source: Union[ProbInput, Tuple[float, float]] = (-1.0, 1.0),
    ) -> np.ndarray:
        """Transform a sample from another input model to this one.

        Parameters
        ----------
        xx : :class:`numpy:numpy.ndarray`
            The sample points from the source probabilistic input model.
        source : Union[ProbInput, Tuple[float, float]], optional
            The source probabilistic input model, or a tuple ``(lower, upper)``
            specifying the bounds of a hypercube with independent uniform
            marginals. The default is ``(-1.0, 1.0)``.

        Returns
        -------
        :class:`numpy:numpy.ndarray`
            The transformed sample in the domain of this probabilistic input
            model.
        """
        source_ = self._prepare_transform(xx, source)

        return source_.transform_to(xx, self)

    def pdf(self, xx: np.ndarray) -> np.ndarray:
        """Compute the probability density function of the probabilistic input.

        Parameters
        ----------
        xx : :class:`numpy:numpy.ndarray`
            The input values in the support of the distribution,
            a two-dimensional array of shape :math:`(N, m)` where :math:`N`
            and :math:`m` are the number of sample points and the dimension,
            respectively. A one-dimensional array of length :math:`m` is also
            accepted and interpreted as a single sample point.

        Returns
        -------
        :class:`numpy:numpy.ndarray`
            The probability density function (PDF) values at the input values.
            The output is a one-dimensional array of length :math:`N`.
        """
        if self.copulas:
            raise ValueError("Copulas are not currently supported!")

        xx = np.atleast_2d(xx)

        if xx.shape[1] != self.dimension:
            raise ValueError(
                f"Input dimension {xx.shape[1]} does not match "
                f"ProbInput dimension {self.dimension}"
            )

        log_pdf = np.zeros(xx.shape[0])
        with np.errstate(divide="ignore"):
            # Use log-transform because of the smallness of numbers
            for i, marginal in enumerate(self.marginals):
                log_pdf += np.log(marginal.pdf(xx[:, i]))

        return np.exp(log_pdf)

    def cdf(self, xx: np.ndarray) -> np.ndarray:
        """Compute the cumulative distribution function of the input.

        Parameters
        ----------
        xx : :class:`numpy:numpy.ndarray`
            The input values in the support of the distribution,
            a two-dimensional array of shape :math:`(N, m)` where :math:`N`
            and :math:`m` are the number of sample points and the dimension,
            respectively. A one-dimensional array of length :math:`m` is also
            accepted and interpreted as a single sample point.

        Returns
        -------
        :class:`numpy:numpy.ndarray`
            The cumulative distribution function (CDF) values
            at the input values. The output is a one-dimensional array
            of length :math:`N`.
        """
        if self.copulas:
            raise ValueError("Copulas are not currently supported!")

        xx = np.atleast_2d(xx)

        if xx.shape[1] != self.dimension:
            raise ValueError(
                f"Input dimension {xx.shape[1]} does not match "
                f"ProbInput dimension {self.dimension}"
            )

        log_cdf = np.zeros(xx.shape[0])
        with np.errstate(divide="ignore"):
            # Use log-transform because of the smallness of numbers
            for i, marginal in enumerate(self.marginals):
                log_cdf += np.log(marginal.cdf(xx[:, i]))

        return np.exp(log_cdf)

    # --- Dunder methods
    def __eq__(self, other: Any) -> bool:
        """Check if two ProbInput instances are equal in value.

        An equality in value between two instances of `ProbInput` means that:

        - All the marginals are equal
        - The copulas are equal
        - The names are equal

        Parameters
        ----------
        other : Any
            The other instance to compare with.

        Returns
        -------
        bool
            ``True`` if the instances are equal in value, ``False`` otherwise.
        """
        if not isinstance(other, ProbInput):
            return False

        if self.name != other.name:
            return False

        if self.copulas != other.copulas:
            return False

        if self.dimension != other.dimension:
            return False

        for m_self, m_other in zip(self.marginals, other.marginals):
            if m_self != m_other:
                return False

        return True

    def __repr__(self):
        """Return the unambiguous string representation of the instance."""
        class_name = self.__class__.__name__
        # Get the value of the constructor arguments
        attrs = {
            "marginals": self.marginals,
            "copulas": self.copulas,
            "name": self.name,
        }
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())

        return f"{class_name}({attrs_str})"

    def __str__(self):
        """Return a human-readable string representation of the instance."""
        if self.name is None or self.name == "":
            table = f"Dimension : {self.dimension}\n"
        else:
            table = f"Name      : {self.name}\n"
            table += f"Dimension : {self.dimension}\n"
        table += "Marginals :\n\n"

        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        rows = []
        for i, m in enumerate(self.marginals):
            row: List[Any] = [i + 1]
            for field_name in FIELD_NAMES:
                attr_value = getattr(m, field_name)
                if attr_value is None:
                    attr_value = "-"
                row.append(attr_value)
            rows.append(row)

        # Create a table of marginals details
        table += tabulate(
            rows,
            headers=header_names,
            stralign="center",
            disable_numparse=True,
        )

        if self.dimension == 1:
            return table

        # Temporary solution for independence copula
        copulas = "Independence" if self.copulas is None else self.copulas

        table += f"\n\nCopulas         : {copulas}"

        return table

    # --- Private utilities
    def _prepare_transform(
        self,
        xx: np.ndarray,
        other: Union[ProbInput, Tuple[float, float]],
    ) -> "ProbInput":
        """Prepare the transformation counterpart as a ProbInput instance.

        Parameters
        ----------
        xx : :class:`numpy:numpy.ndarray`
            The sample points to transform.
        other : Union[ProbInput, Tuple[float, float]]
            The other instance for transformation, either as the source or
            target. If the input is a tuple, it is assumed to be the parameters
            of a uniform distribution (i.e., its lower and upper bounds).

        Returns
        -------
        ProbInput
            The prepared ProbInput instance for transformation.
        """
        if not isinstance(other, ProbInput):
            other_ = ProbInput.replicate(
                self.dimension,
                distribution="uniform",
                parameters=other,
            )
        else:
            other_ = other

        # Make sure the dimensions of the inputs are consistent
        if xx.shape[1] != self.dimension or xx.shape[1] != other_.dimension:
            raise ValueError(
                f"The dimensions of the input samples ({xx.shape[1]}) and "
                f"the probabilistic input models "
                f"({self.dimension}, {other_.dimension}) do not match."
            )

        return other_
