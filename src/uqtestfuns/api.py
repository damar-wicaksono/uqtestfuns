from __future__ import annotations

from typing import Dict, List, Optional, Union

from tabulate import tabulate as tbl

from uqtestfuns.core.registry.registry_entry import UQTestFunInfo
from uqtestfuns.core.registry import _registry

SUPPORTED_TAGS = (
    "sensitivity",
    "optimization",
    "metamodeling",
    "reliability",
    "integration",
)


def list_functions(
    input_dimension: Optional[Union[str, int]] = None,
    output_dimension: Optional[int] = None,
    parameterized: Optional[bool] = None,
    tag: Optional[str] = None,
    tabulate: bool = True,
    tablefmt: str = "grid",
    *,
    entries: Dict[str, UQTestFunInfo] = _registry.entries,
) -> Optional[Union[List[str], str]]:
    """List available test functions from a registry entries dictionary."""

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
            if bool(entry.available_parameter_ids) != parameterized:
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
        row = [i + 1, name + "()"]
        if show_input_dim:
            if entry.variable_dimension:
                dim_str = "M"
            else:
                dim_str = str(entry.input_dimension)
            row.append(dim_str)
        if show_output_dim:
            row.append(entry.output_dimension)
        if show_param:
            row.append(bool(entry.available_parameter_ids))
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
