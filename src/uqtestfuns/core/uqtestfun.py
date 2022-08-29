"""
uqtestfun_abc.py

This module contains the abstract base class for the UQ test functions.
"""
from dataclasses import dataclass, field
import numpy as np

from .utils import create_canonical_uniform_input
from .prob_input.multivariate_input import MultivariateInput
from typing import Any, Callable
from inspect import signature

__all__ = ["UQTestFun"]


@dataclass
class UQTestFun:
    """A dataclass for UQ test functions."""
    evaluate: Callable
    input: MultivariateInput
    spatial_dimension: int = field(init=False)
    name: str = None
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
            max_value: float = 1.0
    ) -> np.ndarray:
        """Transform sample values from a uniform domain to the function domain.

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
        out = f"Name              : {self.name}\n" \
              f"Spatial dimension : {self.spatial_dimension}\n" \
              f"Evaluate          : {self.evaluate.__module__}{signature(self.evaluate)}"

        return out


# @dataclas
# class UQTestFun():
#     """The abstract class for UQ test functions."""
#     _spatial_dimension = None
#     _input = None
#     _parameters = None
#
#     @property
#     def spatial_dimension(self):
#         """The number of input variables (spatial dim.) of the function."""
#         return self._spatial_dimension
#
#     @property
#     def input(self):
#         """The probabilistic input to the test function."""
#         return self._input
#
#     @input.setter
#     def input(self, value):
#         self._input = value
#
#     @property
#     def parameters(self):
#         """The parameters passed to the test function."""
#         self._parameters
#
#     @parameters.setter
#     def parameters(self, value):
#         self._parameters = value
#
#     def transform_inputs(
#             self,
#             xx: np.ndarray,
#             min_value: float = -1.0,
#             max_value: float = 1.0
#     ) -> np.ndarray:
#         """Transform sample values from a uniform domain to the function domain.
#
#         Parameters
#         ----------
#         xx : np.ndarray
#             Sampled input values (realizations) in a uniform domain.
#             By default, the uniform domain is [-1, 1].
#         min_value : float, optional
#             Minimum value of the uniform domain. Default value is -1.0.
#         max_value : float, optional
#             Maximum value of the uniform domain. Default value is 1.0.
#
#         Returns
#         -------
#         np.ndarray
#             Transformed sampled values from the specified uniform domain to
#             the domain of the function as defined the `input` property.
#         """
#         # TODO: Verify input
#
#         # Create an input in the canonical uniform domain
#         canonical_input = create_canonical_uniform_input(
#             self.spatial_dimension, min_value, max_value
#         )
#
#         # Transform the sampled value to the function domain
#         xx_trans = canonical_input.transform_sample(self.input, xx)
#
#         return xx_trans
#
#     @abc.abstractmethod
#     def evaluate(self, xx: np.ndarray, *args, **kwargs):
#         """Abstract method for the test function evaluation."""
#         pass
#
#     def __call__(self, xx: np.ndarray, *args, **kwargs):
#         """Evaluation of the test function by calling the object."""
#
#         return self.evaluate(xx)
