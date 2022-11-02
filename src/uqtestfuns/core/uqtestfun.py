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


def get_fun_str(fun: Callable):
    """Get a string representation of a test function."""
    out = f"{fun.__module__}.{fun.__name__}{signature(fun)}"

    return out


@dataclass
class UQTestFun:
    """A dataclass for UQ test functions.

    Parameters
    ----------
    evaluate : Callable
        Implementation of the a test function as a Callable.
    input : MultivariateInput
        Probabilistic input model.
    name : str, optional
        Name of the instance.
    parameters : Any, optional
        Parameters to the test function.

    Attributes
    ----------
    spatial_dimension : int
        The number of spatial dimension (i.e., input variables) to the test
        function.
    """

    evaluate: Callable
    input: MultivariateInput
    spatial_dimension: int = field(init=False)
    name: Optional[str] = None
    parameters: Any = None

    def __post_init__(self):
        self.spatial_dimension = self.input.spatial_dimension

    def __call__(self, xx: np.ndarray):
        """Evaluation of the test function by calling the instance."""
        if self.parameters is None:
            return self.evaluate(xx)
        else:
            return self.evaluate(xx, self.parameters)

    def transform_inputs(
        self,
        xx: np.ndarray,
        min_value: float = -1.0,
        max_value: float = 1.0,
    ) -> np.ndarray:
        """Transform sample values from a unif. domain to the function domain.

        Parameters
        ----------
        xx : np.ndarray
            Sampled input values (realizations) in a uniform domain.
            By default, the uniform domain is [-1, 1].
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
        # TODO: Verify input

        # Create an input in the canonical uniform domain
        canonical_input = create_canonical_uniform_input(
            self.spatial_dimension, min_value, max_value
        )

        # Transform the sampled value to the function domain
        xx_trans = canonical_input.transform_sample(self.input, xx)

        return xx_trans

    def __str__(self):
        out = (
            f"Name              : {self.name}\n"
            f"Spatial dimension : {self.spatial_dimension}\n"
            f"Evaluate          : {get_fun_str(self.evaluate)}"
        )

        return out
