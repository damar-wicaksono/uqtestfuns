"""
This module provides an abstract base class for defining a test function class.
"""
import abc
import numpy as np

from typing import Optional, Any, Tuple, List

from .prob_input.multivariate_input import MultivariateInput
from .utils import create_canonical_uniform_input

__all__ = ["UQTestFunABC"]


class UQTestFunABC(abc.ABC):
    """An abstract class for UQ test functions.

    Parameters
    ----------
    prob_input : MultivariateInput
        Multivariate probabilistic input model.
    parameters : Any
        Parameters to the test function. Once set, the parameters are held
        constant during function evaluation. It may, however, be modified by
        once an instance has been created.
    name : str, optional
        Name of the instance.

    Attributes
    ----------
    spatial_dimension : int
        The number of spatial dimension (i.e., input variables) to the UQ test
        function. This number is derived directly from ``prob_input``.
    evaluate : Callable
        Implementation of a UQ test function as a Callable.
        Note that when calling an instance of the class on a set of input
        values, the input values are first verified before evaluating them.
    """

    def __init__(
        self,
        prob_input: Optional[MultivariateInput] = None,
        parameters: Optional[Any] = None,
        name: Optional[str] = None,
    ):
        if not (
            prob_input is None or isinstance(prob_input, MultivariateInput)
        ):
            raise TypeError(
                f"Probabilistic input model must be either 'None' or "
                f"of 'MultivariateInput' type! Got instead {type(prob_input)}."
            )

        self._prob_input = prob_input
        self._parameters = parameters
        self._name = name

    @property
    @classmethod
    @abc.abstractmethod
    def tags(cls) -> List[str]:
        """Tags are used to classify different UQ test functions."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def available_inputs(cls) -> Tuple[str, ...]:
        """To store the keys of available probabilistic input specs."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def available_parameters(cls) -> Tuple[str, ...]:
        """To store the keys of available parameterization."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def default_dimension(cls) -> Optional[int]:
        """To store the default dimension of a test function."""
        pass

    @property
    def prob_input(self) -> Optional[MultivariateInput]:
        """The probabilistic input model of the UQ test function."""
        return self._prob_input

    @prob_input.setter
    def prob_input(self, value: MultivariateInput):
        """The setter for probabilistic input model of the UQ test function."""
        if value is None or isinstance(value, MultivariateInput):
            self._prob_input = value
        else:
            raise TypeError(
                f"Probabilistic input model must be either 'None' or "
                f"of 'MultivariateInput' type! Got instead {type(value)}."
            )

    @property
    def parameters(self) -> Any:
        """The parameters of the UQ test function."""
        return self._parameters

    @parameters.setter
    def parameters(self, value: Any):
        self._parameters = value

    @property
    def spatial_dimension(self) -> Optional[int]:
        if self._prob_input is not None:
            return self._prob_input.spatial_dimension
        else:
            return self.default_dimension

    @property
    def name(self) -> str:
        """The name of the UQ test function."""
        return self._name

    def transform_sample(
        self,
        xx: np.ndarray,
        min_value=-1.0,
        max_value=1.0,
    ) -> np.ndarray:
        """Transform sample values from a unif. domain to the func. domain

        Parameters
        ----------
        xx : np.ndarray
            Sampled input values (realizations) in a uniform bounded domain.
            By default, the uniform domain is [-1.0, 1.0].
        min_value : float, optional
            Minimum value of the uniform domain. Default value is -1.0.
        max_value : float, optional
            Maximum value of the uniform domain. Default value is 1.0.

        Returns
        -------
        np.ndarray
            Transformed sampled values from the specified uniform domain to
            the domain of the function as defined the `input` property.
        """
        # Verify the uniform bounds
        assert min_value < max_value, (
            f"min. value ({min_value}) must be "
            f"smaller than max. value ({max_value})!"
        )
        # Verify the sampled input
        _verify_sample_shape(xx, self.spatial_dimension)
        _verify_sample_domain(xx, min_value=min_value, max_value=max_value)

        # Create an input in the canonical uniform domain
        uniform_input = create_canonical_uniform_input(
            self.spatial_dimension, min_value, max_value
        )

        # Transform the sampled value to the function domain
        xx_trans = uniform_input.transform_sample(xx, other=self.prob_input)

        return xx_trans

    @abc.abstractmethod
    def evaluate(self, xx: np.ndarray):
        pass

    def __call__(self, xx: np.ndarray):
        """Evaluation of the test function by calling the instance."""

        # Verify the shape of the input
        _verify_sample_shape(xx, self.spatial_dimension)
        # Verify the domain of the input
        for dim_idx in range(self.spatial_dimension):
            lb = self.prob_input.marginals[dim_idx].lower
            ub = self.prob_input.marginals[dim_idx].upper
            _verify_sample_domain(xx[:, dim_idx], min_value=lb, max_value=ub)

        return self.evaluate(xx)

    def __str__(self):
        out = (
            f"Name              : {self.name}\n"
            f"Spatial dimension : {self.spatial_dimension}"
        )

        return out


def _verify_sample_shape(xx: np.ndarray, num_cols: int):
    """Verify the number of columns of the input sample array.

    Parameters
    ----------
    xx : np.ndarray
        Array of sampled input values with a shape of N-by-M, where N is
        the number of realizations and M is the spatial dimension.
    num_cols : int
        The expected number of columns in the input.

    Raises
    ------
    ValueError
        If the number of columns in the input is not equal to the expected
        number of columns.
    """
    if xx.shape[1] != num_cols:
        raise ValueError(
            f"Wrong dimensionality of the input array!"
            f"Expected {num_cols}, got {xx.shape[1]}."
        )


def _verify_sample_domain(xx: np.ndarray, min_value: float, max_value: float):
    """Verify whether the sampled input values are within the min and max.

    Parameters
    ----------
    xx : np.ndarray
        Array of sampled input values with a shape of N-by-M, where N is
        the number of realizations and M is the spatial dimension.
    min_value : float
        The minimum value of the domain.
    max_value : float
        The maximum value of the domain.

    Raises
    ------
    ValueError
        If any of the input values are outside the domain.
    """
    if not np.all(np.logical_and(xx >= min_value, xx <= max_value)):
        raise ValueError(
            f"One or more values are outside the domain "
            f"[{min_value}, {max_value}]!"
        )
