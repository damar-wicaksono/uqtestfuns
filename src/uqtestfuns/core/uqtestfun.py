"""Module containing the concrete implementation of UQ test functions.

This module provides the UQTestFun class, which encapsulates an evaluation
function, a probabilistic input model, and optional parameters into a single
callable object for uncertainty quantification test functions.
"""

import numpy as np

from typing import Callable, Optional, Union

from .parameters import Parameters
from .prob_input.probabilistic_input_new import ProbInput

__all__ = ["UQTestFun"]


class UQTestFun:
    """A concrete class for UQ test functions.

    Encapsulates an evaluation function, a probabilistic input model,
    optional parameters, and metadata into a single callable object.

    Parameters
    ----------
    evaluate : Callable
        The evaluation function. Must accept a 2D numpy array of shape
        ``(n_samples, input_dimension)`` and return an array of shape
        ``(n_samples,)`` or ``(n_samples, output_dimension)``. If parameters
        are provided, they are passed as keyword arguments.
    prob_input : ProbInput
        The probabilistic input model defining the input space and the
        distribution of the input variables.
    parameters : Parameters, optional
        The parameter set of the UQ test function. If provided, passed as
        keyword arguments to ``evaluate``. Default is None.
    name : str, optional
        The name of the UQ test function. Default is None.
    description : str, optional
        A human-readable description of the UQ test function. Default is None.
    output_dimension : int, optional
        The number of output values produced per input point. Default is 1.

    Raises
    ------
    TypeError
        If any argument has an incorrect type.
    """

    def __init__(
        self,
        evaluate: Callable,
        prob_input: ProbInput,
        parameters: Optional[Parameters] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_dimension: int = 1,
    ):
        if not callable(evaluate):
            raise TypeError("'evaluate' must be callable")
        self._evaluate = evaluate

        if not isinstance(prob_input, ProbInput):
            raise TypeError("'prob_input' must be an instance of ProbInput")
        self._prob_input = prob_input

        if parameters is not None and not isinstance(parameters, Parameters):
            raise TypeError(
                "'parameters' must be an instance of Parameters or None"
            )
        self._parameters = parameters

        self._name = name
        self._description = description
        self._output_dimension = output_dimension

    # --- Public properties
    @property
    def name(self) -> Optional[str]:
        """Get the name of the UQ test function.

        Returns
        -------
        Optional[str]
            The name of the test function, or None if not set.
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """Get the description of the UQ test function.

        Returns
        -------
        Optional[str]
            The description of the test function, or None if not set.
        """
        return self._description

    @property
    def prob_input(self) -> ProbInput:
        """Get the probabilistic input model of the UQ test function.

        Returns
        -------
        ProbInput
            The probabilistic input model that defines the input space
            of the test function.
        """
        return self._prob_input

    @property
    def parameters(self) -> Optional[Parameters]:
        """Get the parameters of the UQ test function.

        Returns
        -------
        Optional[Parameters]
            The parameters of the test function, or None if not set.
        """
        return self._parameters

    @property
    def input_dimension(self) -> int:
        """Get the input dimension of the UQ test function.

        Returns
        -------
        int
            The dimension of the input space, determined by the
            probabilistic input model.
        """
        return self._prob_input.dimension

    @property
    def output_dimension(self) -> int:
        """Get the output dimension of the UQ test function.

        Returns
        -------
        int
            The dimension of the output space, representing the number of
            output values produced by the test function for each input.
        """
        return self._output_dimension

    # --- dunder methods
    def __call__(self, xx: np.ndarray) -> np.ndarray:
        """Evaluate the UQ test function at the given input points.

        Parameters
        ----------
        xx : np.ndarray
            Input array of shape ``(n_samples, input_dimension)``.

        Returns
        -------
        np.ndarray
            Output array of shape ``(n_samples,)`` if ``output_dimension``
            is 1, or ``(n_samples, output_dimension)`` otherwise.

        Raises
        ------
        ValueError
            If the output shape does not match the expected shape.
        """
        # --- Input verification
        self._verify_input(xx)

        # --- Evaluate
        params = self._parameters
        if params is not None:
            yy = self._evaluate(xx, **params)
        else:
            yy = self._evaluate(xx)

        # --- Output verification
        expected_shape = (
            (xx.shape[0],)
            if self._output_dimension == 1
            else (xx.shape[0], self._output_dimension)
        )
        if yy.shape != expected_shape:
            raise ValueError(
                f"Expected output shape {expected_shape}, got {yy.shape}"
            )

        return yy

    def __str__(self) -> str:
        """Return a human-readable summary of the UQ test function."""
        table = f"Name          : {self.name or 'N/A'}\n"
        table += f"Description   : {self.description or 'N/A'}\n"
        table += f"Input dim.    : {self.input_dimension}\n"
        table += f"Output dim.   : {self.output_dimension}\n"

        if self._parameters is not None:
            _params = True
        else:
            _params = False
        table += f"Parameterized : {_params}"

        return table

    def __repr__(self) -> str:
        """Return the unambiguous string representation of the instance.

        The fields shown can be passed to ``create()`` to reconstruct an
        equivalent instance, provided the function is a built-in registered
        function.
        """

        parameters = self.parameters
        if parameters is not None:
            parameters_id = parameters.name
        else:
            parameters_id = None

        return (
            f"<UQTestFun "
            f"name={self.name!r}, "
            f"input_dimension={self.input_dimension}, "
            f"input_id={self.prob_input.name!r}, "
            f"parameters_id={parameters_id!r}"
            f">"
        )

    # --- Public methods
    def get_sample(
        self,
        sample_size: int = 1,
        rng: Union[np.random.Generator, int, None] = None,
    ) -> np.ndarray:
        """Generate a sample of output values from the UQ test function.

        Generates random input points from the probabilistic input model and
        evaluates the test function at those points. Unlike
        ``prob_input.get_sample()``, which returns input samples, this method
        returns the corresponding function output values.

        Parameters
        ----------
        sample_size : int, optional
            The number of sample points to generate. Default is 1.
        rng : Union[np.random.Generator, int, None], optional
            Random number generator or seed for reproducibility. Accepts a
            ``np.random.Generator``, an integer seed, or None for the default
            generator. Default is None.

        Returns
        -------
        np.ndarray
            Output array of shape ``(sample_size,)`` if ``output_dimension``
            is 1, or ``(sample_size, output_dimension)`` otherwise.
        """

        # Generate sample points
        xx = self.prob_input.get_sample(sample_size, rng)

        return self(xx)

    # --- Private methods
    def _verify_input(self, xx: np.ndarray):
        """Verify that the input array is valid for evaluation.

        Performs two validation checks:

        1. Verifies that the input array has the correct shape
           ``(n_samples, input_dimension)``.
        2. Verifies that all input values are within the valid domain
           defined by the probabilistic input model.

        Parameters
        ----------
        xx : np.ndarray
            Input array to validate. Expected shape is
            ``(n_samples, input_dimension)``.

        Raises
        ------
        ValueError
            If the input array is invalid in shape or domain.
        """

        # --- Verify shape
        if not self.prob_input.is_valid_shape(xx):
            raise ValueError(
                f"Expected input array of shape "
                f"(n_samples, {self.input_dimension}), got {xx.shape}."
            )

        # --- Verify domain
        valid = self.prob_input.is_valid_domain(xx)
        if not np.all(valid):
            invalid_samples, invalid_dims = np.where(~valid)
            raise ValueError(
                f"Input values outside the domain at "
                f"sample indices {invalid_samples.tolist()}, "
                f"dimension indices {invalid_dims.tolist()}."
            )
