"""
This module provides abstract base classes for defining a test function class.
"""

import abc
import numpy as np

from copy import deepcopy
from inspect import signature
from typing import Callable, cast, List, Optional

from .prob_input.marginal import Marginal
from .prob_input.probabilistic_input import ProbInput
from .parameters import FunParams
from .custom_typing import (
    ProbInputSpecs,
    ProbInputArgs,
    FunParamSpecs,
    FunParamsArgs,
)
from .utils import create_canonical_uniform_input

__all__ = ["UQTestFunBareABC", "UQTestFunABC"]

CLASS_HIDDEN_ATTRIBUTES = [
    "_tags",
    "_description",
    "_available_inputs",
    "_available_parameters",
    "_default_input_dimension",
]

DEFAULT_DIMENSION = 2


class classproperty(property):  # type: ignore
    """Decorator w/ descriptor to get and set class-level attributes."""

    def __get__(self, owner_self, owner_cls):  # type: ignore
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
    function_id : str, optional
        The ID of the UQ test function. By default, it is None.

    Notes
    -----
    - A bare UQ test function only includes the evaluation function,
      probabilistic input model, parameters, and a (optional) ID.
    """

    def __init__(
        self,
        prob_input: ProbInput,
        parameters: FunParams,
        function_id: Optional[str] = None,
    ):
        self.prob_input = prob_input
        self._parameters = parameters
        self._function_id = function_id
        self._output_dimension: Optional[int] = None

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
    def parameters(self) -> FunParams:
        """The parameters of the UQ test function."""
        return self._parameters

    @parameters.setter
    def parameters(self, value: FunParams):
        """The setter for the parameters of the test function."""
        if not isinstance(value, FunParams):
            raise TypeError(
                f"Expected a 'FunParams' type! Got instead {type(value)}"
            )
        self._parameters = value

    @property
    def function_id(self) -> Optional[str]:
        """The ID of the UQ test function."""
        return self._function_id

    @property
    def input_dimension(self) -> int:
        """The input dimension of the UQ test function."""
        return self.prob_input.input_dimension

    @property
    def output_dimension(self) -> int:
        if self._output_dimension is None:
            xx = self.prob_input.get_sample()
            yy = self(xx)
            if yy.ndim == 1:
                self._output_dimension = 1
            elif yy.ndim == 2:
                self._output_dimension = yy.shape[1]
            else:
                self._output_dimension = yy.shape[1:]
            return self._output_dimension

        return self._output_dimension

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
        _verify_sample_shape(xx, self.input_dimension)
        _verify_sample_domain(xx, min_value=min_value, max_value=max_value)

        # Create an input in the canonical uniform domain
        uniform_input = create_canonical_uniform_input(
            self.input_dimension, min_value, max_value
        )

        # Transform the sampled value to the function domain
        xx_trans = uniform_input.transform_sample(xx, other=self.prob_input)

        return xx_trans

    def __str__(self):
        out = (
            f"Function ID      : {self.function_id}\n"
            f"Input Dimension  : {self.input_dimension}\n"
            f"Output Dimension : {self.output_dimension}\n"
            f"Parameterized    : {bool(self.parameters)}"
        )

        return out

    def __call__(self, xx):
        """Evaluation of the test function by calling the instance."""
        # Verify the shape of the input
        _verify_sample_shape(xx, self.input_dimension)

        # Verify the domain of the input
        for dim_idx in range(self.input_dimension):
            lb = self.prob_input.marginals[dim_idx].lower
            ub = self.prob_input.marginals[dim_idx].upper
            _verify_sample_domain(xx[:, dim_idx], min_value=lb, max_value=ub)

        return self._eval(xx)

    @staticmethod
    @abc.abstractmethod
    def evaluate(xx: np.ndarray, **kwargs) -> np.ndarray:
        """Abstract method for the implementation of the UQ test function."""
        pass

    def _eval(self, xx) -> np.ndarray:
        """Actual computation is delegated to evaluate()."""
        return self.__class__.evaluate(xx, **self.parameters.as_dict())


class UQTestFunABC(UQTestFunBareABC):
    """An abstract class for (published) UQ test functions.

    Parameters
    ----------
    input_dimension : int, optional
        The input dimension of the UQ test function.
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
    function_id : str, optional
        The ID of the UQ test function.
        If not given, `None` is used as the function ID.
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
        If input dimension is specified for a UQ test function with
        a fixed dimension.
    """

    _default_input: Optional[str] = None
    _default_parameters: Optional[str] = None

    def __init__(
        self,
        *,
        input_dimension: Optional[int] = None,
        prob_input_selection: Optional[str] = None,
        parameters_selection: Optional[str] = None,
        function_id: Optional[str] = None,
    ):
        # --- Create a probabilistic input model
        # Select the probabilistic input model
        available_inputs = self.available_inputs
        if not prob_input_selection:
            prob_input_selection = self.default_input
            prob_input_selection = cast(str, prob_input_selection)
        if prob_input_selection not in available_inputs:
            print(prob_input_selection)
            raise KeyError(
                "Input selection is not in the available specifications."
            )

        if self.default_input_dimension is None:
            if not input_dimension:
                input_dimension = DEFAULT_DIMENSION
            prob_input_data = _parse_input_vardim(
                input_dimension,
                prob_input_selection,
                available_inputs,
            )
        else:
            if input_dimension:
                raise TypeError("Fixed test dimension!")
            prob_input_data = _parse_input_fixdim(
                prob_input_selection,
                available_inputs,
            )

        prob_input = ProbInput(**prob_input_data)

        # --- Select the parameters set, when applicable
        if self.available_parameters is None:
            parameters = FunParams()
        else:
            if parameters_selection is None:
                parameter_id = self.default_parameters
            else:
                parameter_id = parameters_selection
            parameters = _create_parameters(
                self.__class__.__name__,
                parameter_id,
                self.available_parameters,
                input_dimension,
            )

        # --- Process the default ID
        if function_id is None:
            function_id = self.__class__.__name__

        # --- Initialize the parent class
        super().__init__(
            prob_input=prob_input,
            parameters=parameters,
            function_id=function_id,
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
    def available_inputs(cls) -> ProbInputSpecs:
        """All the keys to the available probabilistic input specifications."""
        return cls._available_inputs  # type: ignore

    @classproperty
    def default_input(cls) -> Optional[str]:
        """The key to the default probabilistic input specification."""
        return cls._default_input

    @classproperty
    def available_parameters(cls) -> Optional[FunParamSpecs]:
        """All the keys to the available set of parameter values."""
        return cls._available_parameters  # type: ignore

    @classproperty
    def default_parameters(cls) -> Optional[str]:
        """The key to the default set of parameters."""
        return cls._default_parameters  # type: ignore

    @classproperty
    def default_input_dimension(cls) -> Optional[int]:
        """To store the default dimension of a test function."""
        return cls._default_input_dimension  # type: ignore

    @classproperty
    def description(cls) -> Optional[str]:
        """Short description of the UQ test function."""
        return cls._description  # type: ignore

    def __str__(self):
        out = (
            f"Function ID      : {self.function_id}\n"
            f"Input Dimension  : {self.input_dimension}\n"
            f"Output Dimension : {self.output_dimension}\n"
            f"Parameterized    : {bool(self.parameters)}\n"
            f"Description      : {self.description}"
        )

        return out


def _verify_sample_shape(xx: np.ndarray, num_cols: int):
    """Verify the number of columns of the input sample array.

    Parameters
    ----------
    xx : np.ndarray
        Array of sampled input values with a shape of N-by-M, where N is
        the number of realizations and M is the input dimension.
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
        the number of realizations and M is the input dimension.
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


def _parse_input_vardim(
    input_dimension: int,
    input_id: str,
    available_inputs: ProbInputSpecs,
) -> ProbInputArgs:
    """Get the selected input."""
    # Get the input
    raw_data = available_inputs[input_id].copy()

    # Process the marginals
    marginals = []
    for i in range(input_dimension):
        marginal = raw_data["marginals"][0].copy()
        marginal["name"] = f"{marginal['name']}{i}"
        marginals.append(Marginal(**marginal))

    # Recast the type to satisfy type checker
    input_data = cast(ProbInputArgs, raw_data)
    input_data["input_id"] = input_id
    input_data["marginals"] = marginals

    return input_data


def _parse_input_fixdim(
    input_id: str,
    available_inputs: ProbInputSpecs,
) -> ProbInputArgs:
    """Get the selected input."""
    # Get the input
    raw_data = available_inputs[input_id].copy()

    # Process the marginals
    marginals = []
    for marginal in raw_data["marginals"]:
        marginals.append(Marginal(**marginal))

    # Recast the type to satisfy type checker
    input_data = cast(ProbInputArgs, raw_data)
    input_data["input_id"] = input_id
    input_data["marginals"] = marginals

    return input_data


def _create_parameters(
    function_id: str,
    parameter_id: str,
    available_parameters: FunParamSpecs,
    input_dimension: Optional[int] = None,
) -> FunParams:
    """Create the Parameter set of a UQ test function."""

    # Verify if the selection is valid
    if parameter_id not in available_parameters:
        raise KeyError(
            f"Parameter set {parameter_id} is not in the available sets."
        )

    # Must be deepcopied due to modification
    param_dict = deepcopy(available_parameters[parameter_id])

    # Verify if the function_id agrees
    if function_id != param_dict["function_id"]:
        raise ValueError()

    # Prepare the dictionary as input
    param_dict = cast(FunParamsArgs, param_dict)  # Recasting for type checker
    param_dict["parameter_id"] = parameter_id

    # Deal with variable dimension parameter
    declared_parameters = param_dict["declared_parameters"]
    for declared_parameter in declared_parameters:
        value = declared_parameter["value"]
        if isinstance(value, Callable):  # type: ignore
            func_signature = signature(value).parameters
            if "input_dimension" in func_signature:
                parameter_value = value(input_dimension=input_dimension)
                declared_parameter["value"] = parameter_value

    return FunParams(**param_dict)
