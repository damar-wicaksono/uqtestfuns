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
from typing import List, Optional, Tuple, Union, Dict

from .core import UQTestFunABC

__all__ = ["list_functions"]


def list_functions(
    spatial_dimension: Optional[Union[str, int]] = None,
    tag: Optional[str] = None,
    tabulate: bool = True,
) -> Optional[List[UQTestFunABC]]:
    """List of all the available functions.

    Parameters
    ----------
    spatial_dimension : Optional[Union[str, int]]
        Filter based on the number of spatial dimension.
        For variable dimension (i.e., M-dimensional test functions),
        use the string "M".
    tag : Optional[str]
        Filter based on the application tag.
        Supported tags: "metamodeling", "sensitivity", "optimization",
        "reliability".
    tabulate : bool, optional
        The flag whether to print a table on the console or a list
        of the available functions (each in fully-qualified class name).

    Returns
    -------
    Optional[List[UQTestFunABC]]
        Either a tabulated view of the list of available functions,
        or a list of fully-qualified class name (each is callable).
        The function may return None if after filtering there is no entry.

    Notes
    -----
    - When both ``spatial_dimension`` and ``tag`` are specified the results are
      intersected. Entries that satisfy both are returned.
    """

    # --- Parse input arguments
    _verify_input_args(spatial_dimension, tag, tabulate)

    # --- Get all the available classes that implement the test functions
    available_classes: List[Tuple[str, UQTestFunABC]] = get_available_classes(
        test_functions
    )
    available_classes_dict = dict(available_classes)

    # --- Filter according to the requested spatial dimension
    if spatial_dimension:
        available_classes_from_dimension = _get_functions_from_dimension(
            available_classes_dict, spatial_dimension
        )
    else:
        available_classes_from_dimension = list(available_classes_dict.keys())

    # --- Filter according to the requested tag
    if tag:
        available_classes_from_tag = _get_functions_from_tag(
            available_classes_dict, tag.lower()
        )
    else:
        available_classes_from_tag = list(available_classes_dict.keys())

    # --- Combine the results of both filters to obtain the final list
    available_class_names = set(available_classes_from_dimension).intersection(
        set(available_classes_from_tag)
    )

    if not available_class_names:
        return None

    constructors = []

    # --- When asked, immediately return all the fully-qualified class name
    if not tabulate:
        for available_class_name in available_class_names:
            constructor = available_classes_dict[available_class_name]
            constructors.append(constructor)

        return constructors

    # --- Create a tabulated view of the list
    header_names = [
        "No.",
        "Constructor",
        "Spatial Dimension",
        "Application",
        "Description",
    ]

    values = []
    for idx, available_class_name in enumerate(
        sorted(list(available_class_names))
    ):
        available_class = available_classes_dict[available_class_name]

        default_spatial_dimension = available_class.DEFAULT_SPATIAL_DIMENSION
        if not default_spatial_dimension:
            default_spatial_dimension = "M"

        tags = ", ".join(available_class.TAGS)

        description = available_class.DESCRIPTION

        value = [
            idx + 1,
            f"{available_class_name}()",
            f"{default_spatial_dimension}",
            tags,
            f"{description}",
        ]

        values.append(value)

    table = tbl(
        values,
        headers=header_names,
        stralign="center",
        colalign=("center", "center", "center", "center", "left"),
    )

    print(table)

    return None


def _verify_input_args(
    spatial_dimension: Optional[Union[str, int]] = None,
    tag: Optional[str] = None,
    tabulate: bool = True,
) -> None:
    """Verify the input arguments.

    Parameters
    ----------
    spatial_dimension : Optional[Union[str, int]]
        The number of spatial dimension to filter the list.
        For variable dimension (i.e., M-dimensional test functions),
        use the string "M".
    tag : Optional[str]
        The application tag to filter the list.
        Supported tags: "metamodeling", "sensitivity", "optimization",
        "reliability".
    tabulate : bool, optional
        The flag whether to print a table on the console or a list
        of the available functions (each in fully-qualified class name).

    Returns
    ------
    None
        The function exits without any return value when nothing is wrong.

    Raises
    ------
    ValueError
        If ``spatial_dimension`` is not a positive integer or the string "M".
        If ``tag`` is not one of the supported tags.
    TypeError
        If ``spatial_dimension`` is not either an integer, string, or NoneType.
        If ``tag`` is not a string.
        If ``tabulate`` is not a bool.
    """
    # --- Parse 'spatial_dimension'
    if not isinstance(spatial_dimension, (int, str, type(None))):
        raise TypeError(
            f"Invalid type for spatial dimension! "
            f"Expected either an integer or a string. "
            f"Got instead {type(spatial_dimension)}."
        )
    if spatial_dimension is not None and isinstance(spatial_dimension, str):
        if spatial_dimension.lower() != "m":
            raise ValueError(
                f"Invalid value ({spatial_dimension}) for spatial dimension! "
                f"Either a positive integer or 'M' to indicate "
                f"a variable-dimension test function."
            )
    if spatial_dimension is not None and isinstance(spatial_dimension, int):
        if spatial_dimension <= 0:
            raise ValueError(
                f"Invalid value ({spatial_dimension}) for spatial dimension! "
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

    # --- Parse 'tabulate'
    if not isinstance(tabulate, (bool, type(None))):
        raise TypeError(
            f"'tabulate' argument must be of bool type! Got {type(tabulate)}."
        )


def _get_functions_from_dimension(
    available_classes: Dict[str, UQTestFunABC],
    spatial_dimension: Union[int, str],
) -> List[str]:
    """Get the function keys that satisfy the spatial dimension filter."""
    values = []

    # --- Make sure to check against a lower-case string
    if isinstance(spatial_dimension, str):
        spatial_dimension = spatial_dimension.lower()

    for (
        available_class_name,
        available_class_path,
    ) in available_classes.items():
        default_spatial_dimension = (
            available_class_path.DEFAULT_SPATIAL_DIMENSION
        )
        if not default_spatial_dimension:
            default_spatial_dimension = "m"

        if default_spatial_dimension == spatial_dimension:
            values.append(available_class_name)

    return values


def _get_functions_from_tag(
    available_classes: Dict[str, UQTestFunABC], tag: str
) -> List[str]:
    """Get the function keys that satisfy the tag filter."""
    values = []

    for (
        available_class_name,
        available_class_path,
    ) in available_classes.items():
        tags = available_class_path.TAGS

        if tag in tags:
            values.append(available_class_name)

    return values
