from __future__ import annotations

from typing import Dict, List, Optional, Union

from tabulate import tabulate as tbl

from uqtestfuns.core.prob_input.probabilistic_input_new import ProbInput
from uqtestfuns.core.parameters import Parameters
from uqtestfuns.core.uqtestfun import UQTestFun
from uqtestfuns.core.registry.entries import UQTestFunInfo
from uqtestfuns.core.registry import get_registry

SUPPORTED_TAGS = (
    "sensitivity",
    "optimization",
    "metamodeling",
    "reliability",
    "integration",
)


def create(
    name: str,
    input_dimension: Optional[int] = None,
    *,
    input_id: Optional[str] = None,
    parameters_id: Optional[str] = None,
    prob_input: Optional[ProbInput] = None,
    parameters: Optional[Parameters] = None,
) -> UQTestFun:
    """Create a UQ test function instance by name.

    This function retrieves a factory from the registry and uses it to
    instantiate a UQTestFun object with the specified configuration.

    Parameters
    ----------
    name : str
        The name of the test function to create. Must match a built-in UQ test
        function name.
    input_dimension : int, optional
        The number of input dimensions for the test function. Required for
        variable-dimension functions. For fixed-dimension functions, this
        parameter is optional and defaults to the function's specified
        dimension. Default is None.
    input_id : str, optional
        Identifier for selecting the probabilistic input configuration.
        If not specified, the default input ID from the function's
        specification will be used. ``input_id`` and ``prob_input`` are
        mutually exclusive; both cannot be specified at the same time.
        Default is None.
    parameters_id : str, optional
        Identifier for selecting parameter configuration. Required for
        parameterized functions if no default is specified. Ignored for
        non-parameterized functions. ``parameters_id`` and ``parameters`` are
        mutually exclusive; both cannot be specified at the same time.
        Default is None.
    prob_input : ProbInput, optional
        Custom probabilistic input specification to override the default
        or selected input configuration. ``prob_input`` and ``input_id`` are
        mutually exclusive; both cannot be specified at the same time.
        Default is None.
    parameters : Parameters, optional
        Custom parameters object to override the default or selected parameter
        configuration. ``parameters`` and ``parameters_id`` are mutually
        exclusive; both cannot be specified at the same time. Default is None.

    Returns
    -------
    UQTestFun
        A fully configured UQ test function instance.
    """

    factory = get_registry().get_factory(name)

    kwargs = {
        "input_id": input_id,
        "parameters_id": parameters_id,
        "prob_input": prob_input,
        "parameters": parameters,
    }

    if input_dimension is not None:
        return factory(input_dimension, **kwargs)
    else:
        return factory(**kwargs)


def list_functions(
    input_dimension: Optional[Union[str, int]] = None,
    output_dimension: Optional[int] = None,
    parameterized: Optional[bool] = None,
    tag: Optional[str] = None,
    tabulate: bool = True,
    tablefmt: str = "grid",
) -> Optional[Union[List[str], str]]:
    """List available UQ test functions with optional filtering.

    This function queries the registry and returns a list of available
    test functions, optionally filtered by various criteria. Results can
    be displayed as a formatted table or returned as a list of function names.

    Parameters
    ----------
    input_dimension : int or str, optional
        Filter by number of input dimensions. Accepts an integer for
        fixed-dimension functions or 'M' (case-insensitive)
        for variable-dimension functions. If None, no filtering
        by input dimension is applied. Default is None.
    output_dimension : int, optional
        Filter by number of output dimensions. Must be a positive integer.
        If None, no filtering by output dimension is applied. Default is None.
    parameterized : bool, optional
        Filter by parameterization status. If True, only parameterized
        functions are listed. If False, only non-parameterized functions
        are listed. If None, no filtering by parameterization is applied.
        Default is None.
    tag : str, optional
        Filter by application tag. Must be one of the supported tags:
        'sensitivity', 'optimization', 'metamodeling', 'reliability', or
        'integration'. If None, no filtering by tag is applied.
        Default is None.
    tabulate : bool, optional
        If True, print results as a formatted table and return None. If False,
        return a sorted list of function constructor names. Default is True.
    tablefmt : str, optional
        Format for the table output when `tabulate` is True. Follows the
        formats supported by the `tabulate` library (e.g., 'grid', 'html',
        'latex'). Default is 'grid'.

    Returns
    -------
    None, list of str, or str
        - If `tabulate` is True and `tablefmt` is not 'html': prints the table
          and returns None.
        - If `tabulate` is True and `tablefmt` is 'html': returns the table
          as an HTML string.
        - If `tabulate` is False: returns a sorted list of function constructor
          names with parentheses (e.g., ['FunctionName()', ...]).
        - If no functions match the filters: returns None
          (when `tabulate` is True) or an empty list
          (when `tabulate` is False).

    Raises
    ------
    ValueError
        If `tag` is not one of the supported tags, or if `input_dimension` or
        `output_dimension` contains invalid values.
    TypeError
        If any parameter is provided with an incorrect type.

    Notes
    -----
    The table columns displayed depend on the filtering criteria:
    - '# Input' column is shown unless `input_dimension` is specified.
    - '# Output' column is shown only if `output_dimension` is specified.
    - 'Param.' column is shown only if `parameterized` is specified.
    - 'Application' column is shown unless `tag` is specified.
    """

    entries = get_registry().entries

    if tag is not None and tag not in SUPPORTED_TAGS:
        raise ValueError(
            f"Tag {tag!r} is not supported. Choose from {SUPPORTED_TAGS}."
        )

    # Filter entries
    filtered: Dict[str, UQTestFunInfo] = {}
    for name, entry in entries.items():
        if entry.variable_dimension:
            dim_str = "M"
        else:
            dim_str = str(entry.input_dimension)
        if input_dimension is not None:
            if dim_str != str(input_dimension).upper():
                continue
        if output_dimension is not None:
            if entry.output_dimension != output_dimension:
                continue
        if parameterized is not None:
            if bool(entry.available_parameters_ids) != parameterized:
                continue
        if tag is not None:
            if tag not in entry.tags:
                continue
        filtered[name] = entry

    if not tabulate:
        return sorted(name + "()" for name in filtered)

    if not filtered:
        return None

    # Build table rows
    headers = ["No.", "Constructor"]
    show_input_dim = input_dimension is None
    show_output_dim = output_dimension is not None
    show_param = parameterized is not None
    show_tags = tag is None

    if show_input_dim:
        headers.append("# Input")
    if show_output_dim:
        headers.append("# Output")
    if show_param:
        headers.append("Param.")
    if show_tags:
        headers.append("Application")
    headers.append("Description")

    rows = []
    for i, name in enumerate(sorted(filtered)):
        entry = filtered[name]
        row: List[str] = [str(i + 1), name + "()"]
        if show_input_dim:
            if entry.variable_dimension:
                dim_str = "M"
            else:
                dim_str = str(entry.input_dimension)
            row.append(dim_str)
        if show_output_dim:
            if entry.output_dimension is None:
                output_dim = "1"
            else:
                output_dim = str(entry.output_dimension)
            row.append(output_dim)
        if show_param:
            row.append(str(bool(entry.available_parameters_ids)))
        if show_tags:
            row.append(", ".join(entry.tags))
        row.append(entry.description)
        rows.append(row)

    table = tbl(
        rows,
        headers=headers,
        tablefmt=tablefmt,
        maxcolwidths=[None, None] + [20] * (len(headers) - 3) + [30],
    )

    if tablefmt == "html":
        return table

    print(table)

    return None
