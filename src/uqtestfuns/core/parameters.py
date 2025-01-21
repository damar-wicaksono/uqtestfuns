"""
This module contains the implementation of FunParams a class that stores
UQ Test function parameters.
"""

import textwrap

from tabulate import tabulate
from typing import Any, List, Optional

import warnings

__all__ = ["FunParams"]

import numpy as np

from uqtestfuns.core.custom_typing import DeclaredParameters

FIELD_NAMES = ["Keyword", "Value", "Type", "Description"]


class FunParams:
    """A class that stores UQ Test function parameters.

    Parameters
    ----------
    function_id : str, optional.
        The UQ test function ID (typically the name of the test function).
        If not provided, an empty string is used.
    parameter_id : str, optional
        The ID of the parameter set.
        If not provided, an empty string is used.
    description : str, optional
        Descriptive string of the parameter set.
        If not provided, an empty string is used.
    declared_parameters : List[dict], optional
        List of dictionaries containing the UQ test function parameters with
        the following keywords: 'keyword', 'value', 'type', 'description'.
        'keyword' value is a string that appears in the evaluation function.
        The value is None if not provided.
    """

    def __init__(
        self,
        function_id: str = "",
        parameter_id: str = "",
        description: str = "",
        declared_parameters: Optional[DeclaredParameters] = None,
    ):
        self._declared_parameters: dict = {}
        self._dict: dict = {}

        self.function_id = function_id
        self.parameter_id = parameter_id
        self.description = description

        if declared_parameters is None:
            return

        # Parse the declared parameters
        for parameter in declared_parameters:
            self.add(**parameter)

    def __getitem__(self, key: str):
        """Get the current value by name.

        Parameters
        ----------
        key : str
            The name of the parameter, i.e., its keyword. The parameter
            must already be declared.
        """
        return self._dict[key]

    def __setitem__(self, key: str, value: Any):
        """Set the current value by name.

        Parameters
        ----------
        key : str
            The name of the parameter, i.e., its keyword. The parameter must
            already be declared.
        value : Any
            The value of the parameter.

        Notes
        -----
        - This method allows the parameter value to be changed after
          creation.
        """
        if key not in self._dict:
            raise KeyError(f"Parameter '{key}' is not declared")

        self._assert_value_assign(key, value)

        self._dict[key] = value

    def __len__(self) -> int:
        """Return the length of the parameter set."""
        return len(self._declared_parameters)

    def __bool__(self) -> bool:
        """Return True if one or more parameters are declared."""
        return self.__len__() > 0

    def __eq__(self, other) -> bool:
        """Check the equality in value between two instances.

        Parameters
        ----------
        other
            The right-hand side of the operation.

        Notes
        -----
        - Only the equality in the constituent parameters is checked.
        """
        if not isinstance(other, FunParams):
            return False

        a = _nested_dicts_equal(self._dict, other._dict)
        b = _nested_dicts_equal(
            self._declared_parameters,
            other._declared_parameters,
        )

        return a and b

    def __str__(self):
        if not self:
            return str(None)

        table = f"Function ID  : {self.function_id}\n"
        table += f"Parameter ID : {self.parameter_id}\n"
        desc = textwrap.wrap(self.description, width=57)
        # Pad new lines
        if len(desc) > 1:
            desc[1:] = ["               " + line for line in desc[1:]]
        desc_joined = "\n".join(desc)
        table += f"Description  : {desc_joined}\n\n"

        # Get the header names
        header_names = [name.capitalize() for name in FIELD_NAMES]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        list_values = _get_values_as_list(
            self._dict,
            self._declared_parameters,
        )

        table += tabulate(
            list_values,
            headers=header_names,
            stralign="center",
            disable_numparse=True,
        )

        return table

    def as_dict(self):
        """Return key-value pairs of the parameter set."""
        return self._dict

    def add(
        self,
        keyword: str,
        value: Any,
        type: Optional[type] = None,
        description: Optional[str] = "",
    ) -> None:
        """Add a parameter to the parameter set.

        Parameters
        ----------
        keyword : str
            The name of the parameter as it appears in the evaluation function
            signature; must be a valid Python identifier.
        value : Any
            The default value of the parameter.
        type : Optional[type]
            The type of the parameter. If given, the type will be used to
            validate the provided value.
        description : str, optional
            The description of the parameter.
        """
        if keyword in self._declared_parameters:
            raise KeyError(f"Parameter '{keyword}' is already defined")

        if not keyword.isidentifier():
            raise ValueError(
                f"Parameter '{keyword}' is not a valid identifier"
            )

        self._declared_parameters[keyword] = {
            "value": value,
            "type": type,
            "description": description,
        }

        # Verify the value here
        self._assert_value_set(keyword)

        # Update the underlying dict
        self._dict[keyword] = value

    def reset_value(self) -> None:
        """Reset the value of the parameter set to the declared values."""
        self._dict.clear()
        for key, value in self._declared_parameters.items():
            self._dict[key] = value["value"]

    def _assert_value_set(self, keyword: str):
        """Assert the parameter set when they're added the first time.

        Parameters
        ----------
        keyword : str
            The name of the parameter.

        Notes
        -----
        - The type of the value must be consistent with the type (if given).
        """
        type_ = self._declared_parameters[keyword]["type"]
        value = self._declared_parameters[keyword]["value"]
        if type_ is None:
            return

        # When a parameter is first added enforce consistency
        if not isinstance(value, type_):
            raise TypeError(f"Expected {type_} but got {type(value)}")

    def _assert_value_assign(self, keyword, value):
        """Assert the parameter set when they're assigned after creation.

        Parameters
        ----------
        keyword : str
            The name of the parameter.
        value : Any
            The value of the parameter.
        Notes
        -----
        - If the value and the type are not consistent, a warning (but no
          exception is raised).
        """
        type_ = self._declared_parameters[keyword]["type"]
        if type_ is None:
            return

        # When a parameter is assigned, be more forgiving
        if not isinstance(value, type_):
            warnings.warn(
                message=f"Expected {type_} but got {type(value)}",
                category=UserWarning,
                stacklevel=2,
            )


def _nested_dicts_equal(d1, d2) -> bool:
    """Compare the equality in value between two nested dictionaries.

    Parameters
    ----------
    d1
        The first dictionary.
    d2
        The second dictionary

    Returns
    -------
    bool
        True if the dictionaries are equal, False otherwise.
    """
    if not isinstance(d1, dict) or not isinstance(d2, dict):

        # Deal specifically with NumPy array values
        if isinstance(d1, np.ndarray) and isinstance(d2, np.ndarray):
            return np.array_equal(d1, d2)
        return d1 == d2  # Compare values directly if not dictionaries

    if d1.keys() != d2.keys():
        return False  # Different keys

    # Recursively check each key
    return all(_nested_dicts_equal(d1[key], d2[key]) for key in d1)


def _get_values_as_list(
    current_values: dict,
    declared_parameters: dict,
) -> List[List[str]]:
    """

    Parameters
    ----------
    current_values : dict
        The dictionary of current values.
    declared_parameters : dict
        The dictionaries of declared parameters.

    Return
    ------
    List[List[str]]
        List of lists of the relevant data as strings.
    """
    list_values = []
    for i, parameter in enumerate(declared_parameters):
        # Value
        value = current_values[parameter]
        if isinstance(value, np.ndarray):
            value = f"{value.shape} array"
        elif isinstance(value, int):
            value = f"{value:1.5e}"
        elif isinstance(value, float):
            value = f"{value:1.5e}"
        else:
            value = str(value)

        # Type
        type_ = declared_parameters[parameter]["type"]
        if type_ is not None:
            type_ = type_.__name__
        else:
            type_ = "-"

        # Description
        desc = declared_parameters[parameter]["description"]
        if desc == "":
            desc = "-"

        entry = [
            i + 1,
            parameter,
            value,
            type_,
            desc,
        ]

        list_values.append(entry)

    return list_values
