"""
uqtestfun.py

This module contains the dataclass definition for an implementation of a test
function.
"""
from dataclasses import dataclass, field
import numpy as np

from .utils import create_canonical_uniform_input
from .prob_input.multivariate_input import MultivariateInput
from typing import Any, Callable, Optional
from inspect import signature

__all__ = ["UQTestFun"]


@dataclass
class UQTestFun:
    """A dataclass for UQ test functions.

    Parameters
    ----------
    evaluate : Callable
        Implementation of the a test function as a Callable.
    input : MultivariateInput
        Multivariate probabilistic input model.
    name : str, optional
        Name of the instance.
    parameters : Any, optional
        Parameters to the test function.

    Attributes
    ----------
    spatial_dimension : int
        The number of spatial dimension (i.e., input variables) to the test
        function.

    Notes
    -----
    - Even if the probabilistic input model consists of only one marginal,
      a MultivariateInput instance must always be passed.
    """

    evaluate: Callable
    input: MultivariateInput
    spatial_dimension: int = field(init=False)
    name: Optional[str] = None
    parameters: Any = None

    def __post_init__(self):

        if not isinstance(self.input, MultivariateInput):
            raise TypeError(
                f"Input must be of 'MultivariateInput' type, "
                f"instead of {type(self.input)}!"
            )

        self.spatial_dimension = self.input.spatial_dimension

    def __call__(self, xx: np.ndarray):
        """Evaluation of the test function by calling the instance."""

        # Verify the shape of the input
        _verify_sample_shape(xx, self.spatial_dimension)
        # Verify the domain of the input
        for dim_idx in range(self.spatial_dimension):
            lb = self.input.marginals[dim_idx].lower
            ub = self.input.marginals[dim_idx].upper
            _verify_sample_domain(xx[:, dim_idx], min_value=lb, max_value=ub)

        if self.parameters is None:
            return self.evaluate(xx)
        else:
            return self.evaluate(xx, self.parameters)

    def transform_sample(
        self,
        xx: np.ndarray,
        min_value: float = -1.0,
        max_value: float = 1.0,
    ) -> np.ndarray:
        """Transform sample values from a unif. domain to the function domain.

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

        # Verify the sampled input
        _verify_sample_shape(xx, self.spatial_dimension)
        _verify_sample_domain(xx, min_value=min_value, max_value=max_value)

        # Create an input in the canonical uniform domain
        uniform_input = create_canonical_uniform_input(
            self.spatial_dimension, min_value, max_value
        )

        # Transform the sampled value to the function domain
        xx_trans = uniform_input.transform_sample(xx, other=self.input)

        return xx_trans

    def __str__(self):
        out = (
            f"Name              : {self.name}\n"
            f"Spatial dimension : {self.spatial_dimension}\n"
            f"Evaluate          : {_get_fun_str(self.evaluate)}"
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


def _get_fun_str(fun: Callable):
    """Get a string representation of a test function."""
    out = f"{fun.__module__}.{fun.__name__}{signature(fun)}"

    return out
