"""
This module provides abstract base classes for defining a test function class.
"""
import abc
import numpy as np

from inspect import signature
from typing import Any, Callable, Dict, List, Optional, Union

from .prob_input.probabilistic_input import ProbInput
from .prob_input.input_spec import ProbInputSpecFixDim, ProbInputSpecVarDim
from .utils import create_canonical_uniform_input

__all__ = ["UQTestFunBareABC", "UQTestFunABC"]

CLASS_HIDDEN_ATTRIBUTES = [
    "_tags",
    "_description",
    "_available_inputs",
    "_available_parameters",
    "_default_spatial_dimension",
]

DEFAULT_DIMENSION = 2


class classproperty(property):
    """Decorator w/ descriptor to get and set class-level attributes."""

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)  # type: ignore

    def __set__(self, owner_self, owner_cls):  # pragma: no cover
        raise AttributeError("can't set attribute")


class UQTestFunBareABC(abc.ABC):
    """An abstract class for a bare UQ test functions.

    Parameters
    ----------
    prob_input : ProbInput
        The probabilistic input model of the UQ test function.
    parameters : Any, optional
        A set of parameters. By default, it is None.
    name : str, optional
        The name of the UQ test function. By default, it is None.

    Notes
    -----
    - A bare UQ test function only includes the evaluation function,
      probabilistic input model, parameters, and a (optional) name.
    """

    def __init__(
        self,
        prob_input: ProbInput,
        parameters: Optional[Any] = None,
        name: Optional[str] = None,
    ):
        self.prob_input = prob_input
        self._parameters = parameters
        self._name = name

    @property
    def prob_input(self) -> ProbInput:
        """The probabilistic input model of the UQ test function."""
        return self._prob_input

    @prob_input.setter
    def prob_input(self, value: ProbInput):
        """The setter for probabilistic input model of the UQ test function."""
        if isinstance(value, ProbInput):
            self._prob_input = value
        else:
            raise TypeError(
                f"Probabilistic input model must be of "
                f"a 'ProbInput' type! Got instead {type(value)}."
            )

    @property
    def parameters(self) -> Any:
        """The parameters of the UQ test function."""
        return self._parameters

    @parameters.setter
    def parameters(self, value: Any):
        """The setter for the parameters of the test function."""
        self._parameters = value

    @property
    def name(self) -> Optional[str]:
        """The name of the UQ test function."""
        return self._name

    @property
    def spatial_dimension(self) -> int:
        """The spatial dimension of the UQ test function."""
        return self.prob_input.spatial_dimension

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

    def __str__(self):
        out = (
            f"Name              : {self.name}\n"
            f"Spatial dimension : {self.spatial_dimension}"
        )

        return out

    def __call__(self, xx):
        """Evaluation of the test function by calling the instance."""
        # Verify the shape of the input
        _verify_sample_shape(xx, self.spatial_dimension)

        # Verify the domain of the input
        for dim_idx in range(self.spatial_dimension):
            lb = self.prob_input.marginals[dim_idx].lower
            ub = self.prob_input.marginals[dim_idx].upper
            _verify_sample_domain(xx[:, dim_idx], min_value=lb, max_value=ub)

        return self.evaluate(xx)

    @abc.abstractmethod
    def evaluate(self, *args):
        """Abstract method for the implementation of the UQ test function."""
        pass


class UQTestFunABC(UQTestFunBareABC):
    """An abstract class for (published) UQ test functions.

    Parameters
    ----------
    spatial_dimension : int, optional
        The spatial dimension of the UQ test function.
        This is used only when the function supports variable dimension;
        otherwise, if specified, an exception is raised.
        In the case of functions with variable dimension, the default dimension
        is set to 2.
        This is a keyword only parameter.
    prob_input_selection : str, optional
        The selection of probabilistic input model; this is used when there are
        multiple input specifications in the literature.
        This is a keyword only parameter.
    parameters_selection : str, optional
        The selection of parameters set; this is used when there are multiple
        sets of parameters available in the literature.
        This is a keyword only parameter.
    name : str, optional
        The name of the UQ test function.
        If not given, `None` is used as name.
        This is a keyword only parameter.

    Notes
    -----
    - A published UQ test function includes a couple of additional metadata,
      namely tags and description.

    Raises
    ------
    KeyError
        If selection is not in the list of available inputs and parameters.
    TypeError
        If spatial dimension is specified for a UQ test function with
        a fixed dimension.
    """

    _default_input: Optional[str] = None
    _default_parameters: Optional[str] = None

    def __init__(
        self,
        *,
        spatial_dimension: Optional[int] = None,
        prob_input_selection: Optional[str] = None,
        parameters_selection: Optional[str] = None,
        name: Optional[str] = None,
    ):
        # --- Create a probabilistic input model
        # Select the probabilistic input model
        available_inputs = self.available_inputs
        if not prob_input_selection:
            prob_input_selection = self.default_input
        if prob_input_selection not in available_inputs:
            print(prob_input_selection)
            raise KeyError(
                "Input selection is not in the available specifications."
            )
        prob_input_spec = available_inputs[prob_input_selection]

        # Determine the dimensionality of the test function
        if isinstance(prob_input_spec, ProbInputSpecFixDim):
            if spatial_dimension:
                raise TypeError("Fixed test dimension!")
        if not spatial_dimension:
            spatial_dimension = DEFAULT_DIMENSION

        # Create a ProbInput instance
        if isinstance(prob_input_spec, ProbInputSpecVarDim):
            prob_input = ProbInput.from_spec(
                prob_input_spec,
                spatial_dimension=spatial_dimension,
            )
        else:
            prob_input = ProbInput.from_spec(prob_input_spec)

        # --- Select the parameters set, when applicable
        available_parameters = self.available_parameters
        if available_parameters is not None:
            if not parameters_selection:
                parameters_selection = self.default_parameters
            if parameters_selection not in available_parameters:
                raise KeyError(
                    "Parameters selection is not in the available sets."
                )
            parameters = available_parameters[parameters_selection]

            # If the parameters set is a function of spatial dimension
            if isinstance(prob_input_spec, ProbInputSpecVarDim):
                if isinstance(parameters, Callable):  # type: ignore
                    func_signature = signature(parameters).parameters
                    if "spatial_dimension" in func_signature:
                        parameters = parameters(
                            spatial_dimension=spatial_dimension
                        )

        else:
            parameters = None

        # --- Process the default name
        if name is None:
            name = self.__class__.__name__

        # --- Initialize the parent class
        super().__init__(
            prob_input=prob_input, parameters=parameters, name=name
        )

    @classmethod
    def __init_subclass__(cls):
        """Verify if concrete class has all the required hidden attributes.

        Raises
        ------
        NotImplementedError
            If required attributes are not implemented in the concrete class.
        ValueError
            If default input and parameters selections are not specified
            when there are multiple of them.
        KeyError
            If the selections for the default input and parameters set are
            not available.
        """
        for class_hidden_attribute in CLASS_HIDDEN_ATTRIBUTES:
            # Some class attributes must be specified
            if not hasattr(cls, class_hidden_attribute):
                raise NotImplementedError(
                    f"Class {cls} lacks required {class_hidden_attribute!r} "
                    f"class attribute."
                )

        # Parse default input selection
        if cls.default_input:
            if cls.default_input not in cls.available_inputs:
                raise KeyError("Input selection is not available!")
        else:
            if len(cls.available_inputs) > 1:
                raise ValueError(
                    "There are multiple available input specifications, "
                    "the default input selection must be specified!"
                )
            else:
                # If only one is available, use it without being specified
                cls._default_input = list(cls.available_inputs.keys())[0]

        # Parse default parameters set selection
        if cls.available_parameters:
            if cls.default_parameters:
                if cls.default_parameters not in cls.available_parameters:
                    raise KeyError("Parameters selection is not available!")

            else:
                if len(cls.available_parameters) > 1:
                    raise ValueError(
                        "There are multiple available parameters sets, "
                        "the default input selection must be specified!"
                    )
                else:
                    # If only one is available, use it without being specified
                    cls._default_parameters = list(
                        cls.available_parameters.keys()
                    )[0]

    @classproperty
    def tags(cls) -> List[str]:
        """Tags to classify different UQ test functions."""
        return cls._tags  # type: ignore

    @classproperty
    def available_inputs(
        cls,
    ) -> Union[Dict[str, ProbInputSpecFixDim], Dict[str, ProbInputSpecVarDim]]:
        """All the keys to the available probabilistic input specifications."""
        return cls._available_inputs  # type: ignore

    @classproperty
    def default_input(cls) -> Optional[str]:
        """The key to the default probabilistic input specification."""
        return cls._default_input  # type: ignore

    @classproperty
    def available_parameters(cls) -> Optional[Dict[str, Any]]:
        """All the keys to the available set of parameter values."""
        return cls._available_parameters  # type: ignore

    @classproperty
    def default_parameters(cls) -> Optional[str]:
        """The key to the default set of parameters."""
        return cls._default_parameters  # type: ignore

    @classproperty
    def default_spatial_dimension(cls) -> Optional[int]:
        """To store the default dimension of a test function."""
        return cls._default_spatial_dimension  # type: ignore

    @classproperty
    def description(cls) -> Optional[str]:
        """Short description of the UQ test function."""
        return cls._description  # type: ignore

    def __str__(self):
        out = (
            f"Name              : {self.name}\n"
            f"Spatial dimension : {self.spatial_dimension}\n"
            f"Description       : {self.description}"
        )

        return out

    def evaluate(self, xx):
        """Concrete implementation, actual function is delegated to eval_()."""
        if self.parameters is None:
            return self.__class__.eval_(xx)
        else:
            return self.__class__.eval_(xx, self.parameters)

    @staticmethod
    @abc.abstractmethod
    def eval_(*args):  # pragma: no cover
        """Static method for the concrete function implementation.

        Notes
        -----
        - The function evaluation is implemented as a static method so the
          function can be added without being bounded to the instance.
        """
        pass


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
