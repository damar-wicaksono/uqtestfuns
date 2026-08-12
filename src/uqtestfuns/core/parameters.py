"""
Module with an implementation of the `Parameters` class.

This module provides a `Parameters` class for storing and managing a
named set of parameter values for a UQ test function, with optional
per-keyword descriptions. Parameter sets produced by the registry-backed
system are protected (read-only) to preserve their correspondence with
the published source; call `.copy()` to obtain an editable instance.
"""

from __future__ import annotations

import numpy as np
import textwrap

from collections.abc import Mapping, Iterator
from copy import copy, deepcopy
from tabulate import tabulate
from typing import Any, Dict, List, Optional

__all__ = ["Parameters"]


FIELD_NAMES = ["Keyword", "Value", "Type", "Description"]


class Parameters(Mapping):
    """A named bundle of parameter values for a UQ test function.

    The Parameters class stores and manages named parameters with values and
    optional descriptions. Parameter values can be modified in place unless
    the set is protected; sets produced by the registry-backed system
    are protectedto preserve their provenance, while hand-constructed
    or copied sets are not. It supports resolution of dimension-dependent
    parameter values through factory functions.

    Parameters
    ----------
    values : Mapping[str, Any]
        The parameter values, keyed by parameter name. Values must be
        fully resolved at construction time.
    name : str, optional
        The name of the parameter set (e.g., "Ishigami1991"). Defaults
        to None.
    keyword_descriptions : Mapping[str, str], optional
        Per-keyword descriptions. Keys must be a subset of the keys in
        `values`; otherwise a ValueError is raised.
    _protected : bool, optional
        Whether the set is protected against in-place modification. Intended
        for internal use by the registry-backed system; defaults to False.
    """

    def __init__(
        self,
        values: Mapping[str, Any],
        name: Optional[str] = None,
        keyword_descriptions: Optional[Mapping[str, Optional[str]]] = None,
        _protected: bool = False,
    ):
        # --- Assign values
        self._values = dict(values)
        self._name = name
        self._protected = _protected

        # --- Process the keyword descriptions
        kw_desc = dict(keyword_descriptions or {})
        stray = set(kw_desc) - set(self._values.keys())
        if stray:
            raise ValueError(
                f"Keyword descriptions for unknown parameters: {stray}"
            )

        self._keyword_descriptions = {
            key: kw_desc.get(key) for key in self._values
        }

    # --- Properties
    @property
    def name(self) -> Optional[str]:
        """The name of the parameter set.

        Returns
        -------
        str, optional
            The name of the parameter set.
        """
        return self._name

    # --- Public methods
    def copy(self, name: str | None = None) -> "Parameters":
        """Return an independent, unprotected copy safe to modify.

        All values are deep-copied, so editing the returned instance never
        affects the source. Use an explicit ``copy.copy(obj)`` if you
        specifically want a shallow copy.

        Parameters
        ----------
        name : str, optional
            Name for the new instance. Defaults to None (unnamed).

        Returns
        -------
        Parameters
            A new, unprotected Parameters instance.
        """
        new = deepcopy(self)  # routes through __deepcopy__
        if name is not None:
            new._name = name
        return new

    def describe(self, key: str) -> Optional[str]:
        """Get the description of a parameter.

        Parameters
        ----------
        key : str
            The name of the parameter.

        Returns
        -------
        str, optional
            The description of the parameter. If not provided,
            None is returned.
        """
        try:
            return self._keyword_descriptions[key]
        except KeyError as exc:
            raise KeyError(f"Unknown parameter '{key}'") from exc

    # --- Dunder methods
    def __copy__(self) -> "Parameters":
        """Create a shallow copy of the Parameters instance.

        Returns
        -------
        Parameters
            A new Parameters instance with shallow copies of the values
            and keyword descriptions dictionaries.
        """
        values_ = {k: copy(v) for k, v in self._values.items()}
        kw_descriptions = copy(self._keyword_descriptions)
        return Parameters(
            values=values_,
            keyword_descriptions=kw_descriptions,
        )

    def __deepcopy__(self, memo) -> "Parameters":
        """Create a deep copy of the Parameters instance.

        Parameters
        ----------
        memo : dict
            A dictionary of objects already copied during the current
            copying pass.

        Returns
        -------
        Parameters
            A new Parameters instance with deep copies of all values
            and keyword descriptions.
        """
        values_ = {k: deepcopy(v, memo) for k, v in self._values.items()}
        kw_descriptions = deepcopy(self._keyword_descriptions, memo)
        return Parameters(
            values=values_,
            keyword_descriptions=kw_descriptions,
        )

    def __getitem__(self, key: str) -> Any:
        """Get the value of a parameter by name.

        Parameters
        ----------
        key : str
            The name of the parameter.

        Returns
        -------
        Any
            The value of the parameter.
        """
        return self._values[key]

    def __setitem__(self, key: str, value: Any):
        """Set the value of a parameter by name.

        Parameters
        ----------
        key : str
            The name of the parameter.
        value : Any
            The new value for the parameter.

        Raises
        ------
        ParametersProtectedError
            If the parameter set is protected (i.e., comes from the library).
            Protected parameter sets cannot be modified directly; use
            `.copy()` to create an editable copy first.
        KeyError
            If the parameter name does not exist in the parameter set.
        """
        if self._protected:
            raise ParametersProtectedError(
                _format_protection_message(self._name, key)
            )

        self._values[key] = value

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        """Return the number of parameters.

        Returns
        -------
        int
            The number of parameters.
        """
        return len(self._values)

    def __repr__(self):
        """Return the unambiguous string representation of the instance."""
        class_name = self.__class__.__name__
        # Get the value of the constructor arguments
        kw_descriptions = self._keyword_descriptions
        descriptions = {
            k: v for k, v in kw_descriptions.items() if v is not None
        }
        attrs = {
            "values": self._values,  # Avoid returning a copy
            "name": self.name,
            "keyword_descriptions": descriptions,
            "_protected": self._protected,
        }
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())

        return f"{class_name}({attrs_str})"

    def __str__(self):
        """Return a human-readable string representation of the instance."""
        if self.name is None or self.name == "":
            table = "Values :\n\n"
        else:
            table = f"Name   : {self.name}\n"
            table += "Values :\n\n"

        # Get the header names
        field_names = ["Keyword", "Value", "Type", "Description"]
        header_names = [name.capitalize() for name in field_names]
        header_names.insert(0, "No.")

        # Get the values for each field as a list
        rows = _create_list(self._values, self._keyword_descriptions)

        table += tabulate(
            rows,
            headers=header_names,
            colalign=("center", "center", "center", "center", "left"),
            maxcolwidths=[None, None, None, None, 30],
            disable_numparse=True,
        )

        return table


def _create_list(
    values: Dict[str, Any],
    descriptions: Dict[str, Optional[str]],
) -> List[List[str]]:
    """Build table rows from parameter values and descriptions.

    Parameters
    ----------
    values : Dict[str, Any]
        Dictionary of parameter names and their values.
    descriptions : Dict[str, str]
        Dictionary mapping parameter names to descriptions.

    Returns
    -------
    List[List[str]]
        List of rows containing the row number, parameter name,
        formatted value, and description.
    """

    def format_value(val) -> str:
        if isinstance(val, np.ndarray):
            return f"{val.shape} array"
        if isinstance(val, float):
            return f"{val:g}"
        return str(val)

    list_values = []
    for i, (parameter, value) in enumerate(values.items(), start=1):
        desc = textwrap.fill(descriptions.get(parameter) or "-", width=57)
        list_values.append(
            [
                str(i),
                parameter,
                format_value(value),
                type(value).__name__,
                desc,
            ]
        )

    return list_values


class ParametersProtectedError(TypeError):
    """Raised when modifying a library-supplied (protected) parameter set.

    Obtain an editable copy via create_parameters() or .copy() first.
    """


def _format_protection_message(name: str | None, key: str) -> str:
    """Format an error message for protected parameter modification attempts.

    Parameters
    ----------
    name : str, optional
        The name of the parameter set. If None, "<unnamed>" is used.
    key : str
        The name of the parameter that was attempted to be modified.

    Returns
    -------
    str
        A formatted error message explaining why the modification failed
        and how to create an editable copy of the parameter set.
    """
    set_name = name or "<unnamed>"
    return (
        f"\nCannot modify parameter {key!r} of {set_name!r}:\n"
        f"this parameter set comes from the library and is protected\n"
        f"to preserve its correspondence with the published source.\n"
        f"\n"
        f"To experiment with different values, get a working copy \n"
        f"from a an existing function instance:\n"
        f"\n"
        f"    p = f.parameters.copy()\n"
        f"    p[{key!r}] = <new value>\n"
    )
