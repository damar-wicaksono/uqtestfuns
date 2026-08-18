from __future__ import annotations

from typing import Dict, List, Literal, Optional, overload, Union

from tabulate import tabulate as tbl

from uqtestfuns.core.parameters import Parameters
from uqtestfuns.core.prob_input.probabilistic_input import ProbInput
from uqtestfuns.core.registry import get_registry
from uqtestfuns.core.registry.entries import UQTestFunInfo
from uqtestfuns.core.uqtestfun import UQTestFun
from uqtestfuns.global_settings import SUPPORTED_TAGS

__all__ = ["create", "list_functions", "list_parameters"]


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

    _verify_input_args(
        input_dimension, tag, output_dimension, parameterized, tabulate
    )

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
        return sorted(name for name in filtered)

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


@overload
def list_parameters(
    name: str,
    *,
    tabulate: Literal[True],
    tablefmt: str,
) -> None: ...


@overload
def list_parameters(
    name: str,
    *,
    tabulate: Literal[False],
) -> List[str]: ...


def list_parameters(
    name: str,
    *,
    tabulate: bool = True,
    tablefmt: str = "simple",
) -> Optional[List[str]]:
    """Display parameter information for a UQ test function.

    This function prints information about the parameters of a specified
    test function, including parameter keywords and available parameter sets.

    Parameters
    ----------
    name : str
        The name of the test function to query.
    tabulate : bool, optional
        If ``True``, print results as a formatted table and return ``None``.
        If ``False``, return a sorted list of parameter set names.
        Default is ``True``.
    tablefmt : str, optional
        Format for the table output when ``tabulate`` is True. Follows the
        formats supported by the ``tabulate`` library. Default is 'simple'.

    Returns
    -------
    None or List[str]
        If ``tabulate`` is ``True`` the function prints the result directly
        to stdout. If ``tabulate`` is ``False``, it returns a sorted list of
        parameter set names for the given function.
    """

    # Get the test function information
    reg = get_registry()
    info = reg[name]

    if not tabulate:
        return sorted(info.available_parameters_ids.keys())

    # Skip if the function is not parameterized
    if info.default_parameters_id is None:
        print(f"\n{name} has no parameters.")
        return None

    header = f"Parameters for {name}"
    print(f"\n{header}")
    print("=" * len(header))

    available_ids = info.available_parameters_ids
    headers = ["No", "ID", "Description"]
    rows = [
        [i + 1, param_id, desc or "—"]
        for i, (param_id, desc) in enumerate(available_ids.items())
    ]

    out = tbl(
        rows,
        headers=headers,
        tablefmt=tablefmt,
        colalign=("center", "left", "left"),
        maxcolwidths=[None, None, 50],
        disable_numparse=True,
    )
    out += f"\nDefault: {info.default_parameters_id}"

    print(out)

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
