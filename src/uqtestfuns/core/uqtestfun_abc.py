"""
This module provides abstract base classes for defining a test function class.
"""

import abc
from abc import ABC

import numpy as np

from copy import deepcopy
from inspect import signature
from typing import Callable, cast, List, Optional, Tuple, Type, Union

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

__all__ = [
    "UQTestFunBareABC",
    "UQTestFunABC",
    "UQTestFunFixDimABC",
    "UQTestFunVarDimABC",
]

CLASS_HIDDEN_ATTRIBUTES = [
    "_tags",
    "_description",
    "_available_inputs",
    "_available_parameters",
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
    def output_dimension(self) -> Union[int, Tuple[int, ...]]:
        """The output dimension of the UQ test function."""
        xx = self.prob_input.get_sample()
        yy = self(xx)
        if yy.ndim == 1:
            output_dim = 1
        elif yy.ndim == 2:
            output_dim = yy.shape[1]
        else:
            output_dim = yy.shape[1:]

        return output_dim

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


class UQTestFunABC(UQTestFunBareABC, ABC):
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
    input_id : str, optional
        The selection of probabilistic input model; this is used when there are
        multiple input specifications in the literature.
        This is a keyword only parameter.
    parameters_id : str, optional
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

    _default_input_id: Optional[str] = None
    _default_parameters_id: Optional[str] = None

    @classproperty
    def tags(cls) -> List[str]:
        """Tags to classify different UQ test functions."""
        return cls._tags  # type: ignore

    @classproperty
    def available_inputs(cls) -> ProbInputSpecs:
        """All the keys to the available probabilistic input specifications."""
        return cls._available_inputs  # type: ignore

    @classproperty
    def default_input_id(cls) -> Optional[str]:
        """The key to the default probabilistic input specification."""
        return cls._default_input_id  # type: ignore

    @classproperty
    def available_parameters(cls) -> Optional[FunParamSpecs]:
        """All the keys to the available set of parameter values."""
        return cls._available_parameters  # type: ignore

    @classproperty
    def default_parameters_id(cls) -> Optional[str]:
        """The key to the default set of parameters."""
        return cls._default_parameters_id  # type: ignore

    @classproperty
    def description(cls) -> Optional[str]:
        """Short description of the UQ test function."""
        return cls._description  # type: ignore

    @property
    @abc.abstractmethod
    def variable_dimension(self):
        pass

    def __str__(self):
        if self.variable_dimension:
            input_dimension = f"{self.input_dimension} (variable)"
        else:
            input_dimension = f"{self.input_dimension} (fixed)"
        tags = ", ".join(self.tags)
        out = (
            f"Function ID      : {self.function_id}\n"
            f"Input Dimension  : {input_dimension}\n"
            f"Output Dimension : {self.output_dimension}\n"
            f"Parameterized    : {bool(self.parameters)}\n"
            f"Description      : {self.description}\n"
            f"Applications     : {tags}"
        )

        return out

    def _verify_input_id(self, input_id: Optional[str]) -> str:
        """Verify the 'input_id' argument.

        Parameters
        ----------
        input_id : Optional[str]
            The ID of the probabilistic input specification.

        Returns
        -------
        str
            The verified ID of the probabilistic input specification.
        """
        # --- Verify the input
        if input_id is None:
            input_id = self.default_input_id
            input_id = cast(str, input_id)

        available_inputs = self.available_inputs
        if input_id not in available_inputs:
            raise KeyError(
                f"Input ID {input_id} is not in the available "
                f"specifications {list(available_inputs.keys())}"
            )

        return input_id

    def _verify_parameters_id(self, parameters_id: Optional[str]) -> str:
        """Verify the 'parameters_id' argument.

        Parameters
        ----------
        parameters_id : Optional[str]
            The ID of the function parameters specification.

        Returns
        -------
        str
            The verified ID of the function parameters specification.
        """
        available_parameters = self.available_parameters

        if self.available_parameters is None and parameters_id is not None:
            raise ValueError("No parameters are available")

        if self.available_parameters is None:
            return ""

        if parameters_id is None:
            parameters_id = self.default_parameters_id
            parameters_id = cast(str, parameters_id)

        if parameters_id not in available_parameters:
            raise KeyError(
                f"Input ID {parameters_id} is not in the available "
                f"specifications {list(available_parameters.keys())}"
            )

        return parameters_id


class UQTestFunFixDimABC(UQTestFunABC, ABC):
    """An abstract class for (published) fixed-dimension UQ test functions.

    Parameters
    ----------
    input_id : str, optional
        The selection of probabilistic input model; this is used when there are
        multiple input specifications in the literature.
        This is a keyword only parameter.
    parameters_id : str, optional
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

    def __init__(
        self,
        *,
        input_id: Optional[str] = None,
        parameters_id: Optional[str] = None,
        function_id: Optional[str] = None,
    ):
        # --- Create a probabilistic input model
        input_id = self._verify_input_id(input_id)
        prob_input = self._create_prob_input(input_id)

        # --- Create a set of function parameters
        parameters_id = self._verify_parameters_id(parameters_id)
        fun_params = self._create_fun_params(parameters_id)

        # --- Process the default ID
        if function_id is None:
            function_id = self.__class__.__name__

        # --- Initialize the parent class
        super().__init__(
            prob_input=prob_input,
            parameters=fun_params,
            function_id=function_id,
        )

    def __init_subclass__(cls, **kwargs):
        """Verify if concrete class has all the required hidden attributes."""
        _init_subclass(cls)

    @property
    def variable_dimension(self) -> bool:
        """Return ``False`` due to fixed dimension function."""
        return False

    def _create_prob_input(self, input_id: str) -> ProbInput:
        """Create an instance of probabilistic input.

        Parameters
        ----------
        input_id : str
            The ID of the available probabilistic input models.

        Returns
        -------
        ProbInput
            The probabilistic input model based on the selected ID.
        """
        # Get the input (copy to avoid mutation)
        raw_data = deepcopy(self.available_inputs[input_id])

        # Process the marginals
        marginals = []
        for marginal in raw_data["marginals"]:
            marginals.append(Marginal(**marginal))

        # Recast the type to satisfy type checker
        input_data = cast(ProbInputArgs, raw_data)
        input_data["input_id"] = input_id
        input_data["marginals"] = marginals

        return ProbInput(**input_data)

    def _create_fun_params(self, parameters_id: Optional[str]) -> FunParams:
        """Create an instance of function parameters.

        Parameters
        ----------
        parameters_id : str
            The ID of the available function parameters.

        Returns
        -------
        FunParams
            The set of function parameters based on the selected ID.
        """
        if self.available_parameters is None:
            return FunParams()

        # Must be deep-copied due to modification
        param_data = deepcopy(self.available_parameters[parameters_id])

        # Prepare the dictionary as input
        param_data = cast(FunParamsArgs, param_data)  # for type checker
        param_data["parameter_id"] = parameters_id

        return FunParams(**param_data)


class UQTestFunVarDimABC(UQTestFunABC, ABC):
    """An abstract class for (published) variable-dimension UQ test functions.

    Parameters
    ----------
    input_dimension : int, optional
        The input dimension of the UQ test function.
        This is used only when the function supports variable dimension;
        otherwise, if specified, an exception is raised.
        In the case of functions with variable dimension, the default dimension
        is set to 2.
    input_id : str, optional
        The selection of probabilistic input model; this is used when there are
        multiple input specifications in the literature.
        This is a keyword only parameter.
    parameters_id : str, optional
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

    def __init__(
        self,
        input_dimension: int = DEFAULT_DIMENSION,
        *,
        input_id: Optional[str] = None,
        parameters_id: Optional[str] = None,
        function_id: Optional[str] = None,
    ):
        # --- Create a probabilistic input model
        input_id = self._verify_input_id(input_id)
        prob_input = self._create_prob_input(input_id, input_dimension)

        # --- Select the parameters set, when applicable
        parameters_id = self._verify_parameters_id(parameters_id)
        fun_params = self._create_fun_params(parameters_id, input_dimension)

        # --- Process the default ID
        if function_id is None:
            function_id = self.__class__.__name__

        # --- Initialize the parent class
        super().__init__(
            prob_input=prob_input,
            parameters=fun_params,
            function_id=function_id,
        )

    def __init_subclass__(cls, **kwargs):
        """Verify if concrete class has all the required hidden attributes."""
        _init_subclass(cls)

    @property
    def variable_dimension(self) -> bool:
        return True

    def _create_prob_input(self, input_id: str, input_dim: int) -> ProbInput:
        """Create an instance of probabilistic input model.

        Parameters
        ----------
        input_id : str
            The ID of the available probabilistic input models.
        input_dim : int
            The input dimension of the UQ test function.

        Returns
        -------
        ProbInput
            The probabilistic input model based on the selected ID.
        """

        # Get the input
        raw_data = deepcopy(self.available_inputs[input_id])

        # Process the marginals
        marginal = raw_data["marginals"]
        if callable(marginal):
            # Marginal specification is given as a function
            marginals = marginal(input_dim)
            marginals = [Marginal(**marginal) for marginal in marginals]
        else:
            # Marginal specification will be spawned up to the # of dimension
            marginals = []
            for i in range(input_dim):
                marginal = raw_data["marginals"][0].copy()
                marginal["name"] = f"{marginal['name']}{i+1}"
                marginals.append(Marginal(**marginal))

        # Recast the type to satisfy type checker
        input_data = cast(ProbInputArgs, raw_data)
        input_data["input_id"] = input_id
        input_data["marginals"] = marginals

        return ProbInput(**input_data)

    def _create_fun_params(
        self,
        parameters_id: Optional[str],
        input_dim: int,
    ) -> FunParams:
        """Create an instance of function parameters.

        Parameters
        ----------
        parameters_id : str
            The ID of the available function parameters.
        input_dim : int
            The input dimension of the UQ test function.

        Returns
        -------
        FunParams
            The set of function parameters based on the selected ID.
        """

        if self.available_parameters is None:
            return FunParams()

        # Must be deep-copied due to modification
        param_data = deepcopy(self.available_parameters[parameters_id])

        # Prepare the dictionary as input
        param_data = cast(FunParamsArgs, param_data)  # for type checker
        param_data["parameter_id"] = parameters_id

        # Deal with variable dimension parameter
        declared_parameters = param_data["declared_parameters"]
        for declared_parameter in declared_parameters:
            value = declared_parameter["value"]
            if isinstance(value, Callable):  # type: ignore
                func_signature = signature(value).parameters
                if "input_dimension" in func_signature:
                    parameter_value = value(input_dimension=input_dim)
                    declared_parameter["value"] = parameter_value

        return FunParams(**param_data)


def _init_subclass(cls: Type[UQTestFunABC]):
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
    if cls.default_input_id:
        if cls.default_input_id not in cls.available_inputs:
            raise KeyError("Input selection is not available!")
    else:
        if len(cls.available_inputs) > 1:
            raise ValueError(
                "There are multiple available input specifications, "
                "the default input selection must be specified!"
            )
        else:
            # If only one is available, use it without being specified
            cls._default_input_id = list(cls.available_inputs.keys())[0]

    # Parse default parameters set selection
    if cls.available_parameters:
        if cls.default_parameters_id:
            if cls.default_parameters_id not in cls.available_parameters:
                raise KeyError("Parameters selection is not available!")

        else:
            if len(cls.available_parameters) > 1:
                raise ValueError(
                    "There are multiple available parameters sets, "
                    "the default input selection must be specified!"
                )
            else:
                # If only one is available, use it without being specified
                cls._default_parameters_id = list(
                    cls.available_parameters.keys()
                )[0]


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
