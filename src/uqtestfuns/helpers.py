"""
Module providing high-level helper functions.

Notes
-----
- High-level functions typically contain many guardrails against invalidity
  of the input arguments.
"""

from tabulate import tabulate as tbl  # 'tabulate' is used as a parameter name
from .utils import get_available_classes, SUPPORTED_TAGS
from . import test_functions
from typing import List, Optional, Union

from .core import UQTestFunABC

__all__ = ["list_functions"]


HEADER: dict = {
    "input_dim": {
        "header_name": "# Input",
        "colalign": "center",
        "maxcolwidth": None,
    },
    "output_dim": {
        "header_name": "# Output",
        "colalign": "center",
        "maxcolwidth": None,
    },
    "parameterized": {
        "header_name": "Param.",
        "colalign": "center",
        "maxcolwidth": None,
    },
    "tags": {
        "header_name": "Application",
        "colalign": "center",
        "maxcolwidth": 20,
    },
    "description": {
        "header_name": "Description",
        "colalign": "left",
        "maxcolwidth": 30,
    },
}


def list_functions(
    input_dimension: Optional[Union[str, int]] = None,
    tag: Optional[str] = None,
    output_dimension: Optional[int] = None,
    parameterized: Optional[bool] = None,
    tabulate: bool = True,
    tablefmt: str = "grid",
) -> Optional[Union[List[UQTestFunABC], str]]:
    """List of all the available functions.

    Parameters
    ----------
    input_dimension : Optional[Union[str, int]]
        Filter based on the number of input dimension.
        For variable dimension (i.e., M-dimensional test functions),
        use the string "M".
    tag : Optional[str]
        Filter based on the application tag.
        Supported tags: "metamodeling", "sensitivity", "optimization",
        "reliability".
    output_dimension : Optional[Union[str, int]]
        Filter based on the number of output dimension.
    parameterized : bool, optional
        Filter based on whether the test function is parameterized.
    tabulate : bool, optional
        The flag whether to print a table on the console or a list
        of the available functions (each in fully-qualified class name).
    tablefmt : str, optional
        Format of the table output; use "html" to return a table in HTML
        format nicely rendered in Jupyter notebook.

    Returns
    -------
    Optional[List[UQTestFunABC]]
        Either a tabulated view of the list of available functions,
        or a list of fully-qualified class name (each is callable).
        The function may return None if after filtering there is no entry.

    Notes
    -----
    - When both ``input_dimension`` and ``tag`` are specified the results are
      intersected. Entries that satisfy both are returned.
    """

    # --- Parse input arguments
    _verify_input_args(
        input_dimension, tag, output_dimension, parameterized, tabulate
    )

    # --- Parse the module-level data
    data = _parse_modules_data(test_functions)

    # --- Filter based on the input dimension
    data = _filter_on_input_dim(data, input_dimension)

    # --- Filter based on the output dimension
    data = _filter_on_output_dim(data, output_dimension)

    # --- Filter based on parameterization
    data = _filter_on_parameterized(data, parameterized)

    # --- Filter based on the tags
    data = _filter_on_tag(data, tag)

    # --- When asked, immediately return all the fully-qualified class name
    if not tabulate:
        constructors = [
            data[k]["full_path"] for k in sorted(list(data.keys()))
        ]
        return constructors

    # --- Get the arguments for tabulate
    print_attribs, header_names, colalign, maxcolwidth = _get_table_formatting(
        input_dimension,
        tag,
        output_dimension,
        parameterized,
    )

    values = _create_list_values(data, print_attribs)

    if len(values) == 0:
        return None

    if tablefmt == "html":
        colalign[-1] = "center"
        table = tbl(
            values,
            headers=header_names,
            tablefmt=tablefmt,
            colalign=colalign,
            maxcolwidths=maxcolwidth,
        )
        return table
    else:
        table = tbl(
            values,
            headers=header_names,
            tablefmt=tablefmt,
            colalign=colalign,
            maxcolwidths=maxcolwidth,
        )
        print(table)

    return None


def _verify_input_args(
    input_dimension: Optional[Union[str, int]] = None,
    tag: Optional[str] = None,
    output_dimension: Optional[int] = None,
    parameterized: Optional[bool] = None,
    tabulate: bool = True,
) -> None:
    """Verify the input arguments.

    Parameters
    ----------
    input_dimension : Optional[Union[str, int]]
        The number of input dimension to filter the list of test functions.
        For variable dimension (i.e., M-dimensional test functions),
        use the string "M".
    tag : Optional[str]
        The application tag to filter the list of test functions.
        Supported tags: "metamodeling", "sensitivity", "optimization",
        "reliability".
    output_dimension : int, optional
        The number of output dimension to filter the list of test functions.
    parameterized : bool, optional
        The flag based on whether the test function is parameterized to filter
        the list of test functions.
    tabulate : bool, optional
        The flag whether to print a table on the console or a list
        of the available functions (each in fully-qualified class name).

    Raises
    ------
    ValueError
        If ``input_dimension`` is not a positive integer or the string "M".
        If ``tag`` is not one of the supported tags.
        If ``output_dimension`` is not a positive integer.
    TypeError
        If ``input_dimension`` is not either an integer, string, or NoneType.
        If ``tag`` is not a string.
        If ``output_dimension`` is not an integer, string, or NoneType.
        If ``parameterized`` is not a bool.
        If ``tabulate`` is not a bool.
    """
    # --- Parse 'input_dimension'
    if not isinstance(input_dimension, (int, str, type(None))):
        raise TypeError(
            f"Invalid type for input dimension! "
            f"Expected either an integer or a string. "
            f"Got instead {type(input_dimension)}."
        )
    if input_dimension is not None and isinstance(input_dimension, str):
        if input_dimension.lower() != "m":
            raise ValueError(
                f"Invalid value ({input_dimension}) for input dimension! "
                f"Either a positive integer or 'M' to indicate "
                f"a variable-dimension test function."
            )
    if input_dimension is not None and isinstance(input_dimension, int):
        if input_dimension <= 0:
            raise ValueError(
                f"Invalid value ({input_dimension}) for input dimension! "
                f"Either a positive integer or 'M' to indicate "
                f"a variable-dimension test function."
            )

    # --- Parse 'tag'
    if not isinstance(tag, (str, type(None))):
        raise TypeError(f"Tag argument must be of str type! Got {type(tag)}.")
    if tag is not None and tag not in SUPPORTED_TAGS:
        raise ValueError(
            f"Tag {tag!r} is not supported. Use one of {SUPPORTED_TAGS}!"
        )

    # --- Parse 'input_dimension'
    if not isinstance(output_dimension, (int, type(None))):
        raise TypeError(
            f"Invalid type for output dimension! "
            f"Expected either an integer or a string. "
            f"Got instead {type(output_dimension)}."
        )
    if output_dimension is not None:
        if output_dimension <= 0:
            raise ValueError(
                f"Invalid value ({output_dimension}) for output dimension! "
                f"Must be a positive integer."
            )

    # --- Parse 'parameterized'
    if not isinstance(parameterized, (bool, type(None))):
        raise TypeError(
            f"'parameterized' argument must be of bool type! "
            f"Got {type(parameterized)}."
        )

    # --- Parse 'tabulate'
    if not isinstance(tabulate, (bool, type(None))):
        raise TypeError(
            f"'tabulate' argument must be of bool type! Got {type(tabulate)}."
        )


def _filter_on_input_dim(data, input_dimension):
    """Filter the dictionary of test functions data based on the input dim."""
    if input_dimension is not None:
        # Make the input dimension a string and upper case;
        # the result is either a numeric string or the string "M"
        input_dimension = str(input_dimension).upper()
        data = {
            k: v for k, v in data.items() if v["input_dim"] == input_dimension
        }

    return data


def _filter_on_output_dim(data, output_dimension):
    """Filter the dictionary of test functions data based on the output dim."""
    if output_dimension is not None:
        data = {
            k: v
            for k, v in data.items()
            if v["output_dim"] == output_dimension
        }

    return data


def _filter_on_parameterized(data, parameterized):
    """Filter the dictionary of test functions data based on the param."""
    if parameterized is not None:
        data = {
            k: v
            for k, v in data.items()
            if v["parameterized"] is parameterized
        }

    return data


def _filter_on_tag(data, tag):
    """Filter the dictionary of test functions data based on the tag."""
    if tag is not None:
        data = {k: v for k, v in data.items() if tag in v["tags"]}

    return data


def _create_list_values(data, print_attribs):
    """Get the selected values from dictionary test functions data."""
    values = []
    for i, function_name in enumerate(sorted(list(data.keys()))):
        values_tmp = [i + 1, data[function_name]["constructor"]]
        for print_attrib in print_attribs:
            values_tmp.append(data[function_name][print_attrib])
        values.append(values_tmp)

    return values


def _get_table_formatting(
    input_dimension,
    tag,
    output_dimension,
    parameterized,
):
    """Get the table formatting as arguments to 'tabulate()'."""
    header_names: List[str] = ["No.", "Constructor"]
    colalign: List[str] = ["center", "center"]
    maxcolwidth: List[Optional[int]] = [None, None]
    print_attribs: List[str] = []

    # The printed attribute should appear in this order
    if input_dimension is None:
        print_attribs.append("input_dim")

    if output_dimension is None:
        print_attribs.append("output_dim")

    if parameterized is None:
        print_attribs.append("parameterized")

    if tag is None:
        print_attribs.append("tags")

    # --- Always get description
    print_attribs.append("description")

    # --- Get the arguments for tabulate
    for print_attrib in print_attribs:
        header_names.append(HEADER[print_attrib]["header_name"])
        colalign.append(HEADER[print_attrib]["colalign"])
        maxcolwidth.append(HEADER[print_attrib]["maxcolwidth"])

    return print_attribs, header_names, colalign, maxcolwidth


def _parse_modules_data(package):
    available_classes = get_available_classes(package)

    data = {}

    for available_class, class_path in available_classes:

        # Create an instance of test function to parse its properties
        instance: UQTestFunABC = class_path()

        # Get the dimension
        if instance.variable_dimension:
            input_dimension = "M"
        else:
            input_dimension = str(instance.input_dimension)

        data[available_class] = {
            "constructor": available_class + "()",
            "input_dim": input_dimension,
            "output_dim": instance.output_dimension,
            "parameterized": True if instance.parameters else False,
            "tags": ", ".join(instance.tags),
            "description": instance.description,
            "full_path": class_path,
        }

    return data
