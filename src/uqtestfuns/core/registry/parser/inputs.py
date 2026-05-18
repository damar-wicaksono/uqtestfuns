"""Parser for the 'inputs' section in the YAML specifications.

This module provides functionality to parse and validate probabilistic input
specifications from YAML specification files. It processes marginal
distributions defined as lists, templates, or factory references,
and supports input redirection to external YAML files.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from uqtestfuns.core.registry.specs import (
    CallableSpec,
    MarginalSpec,
    MarginalTemplate,
    UQInputSpec,
)

from .utils import parse_factory, safe_load, substitute_idx
from .expression import resolve_numeric
from .validation import (
    SpecValidationError,
    validate_marginal,
    validate_required_keys,
)


def parse_inputs(
    inputs_value: Union[str, dict],
    spec_file: Path,
    pkg_root: Path,
) -> Dict[str, UQInputSpec]:
    """Parse the 'inputs' section from a YAML specification.

    Parameters
    ----------
    inputs_value : Union[str, dict]
        The raw 'inputs' value from the YAML specification.

        Accepted forms:
        - ``dict``: A mapping of input-set names to input specifications.
        - ``str`` ending in ``.yaml``: A relative path to another YAML file
          whose ``inputs`` section should be loaded recursively.

    spec_file : Path
        Path to the YAML specification currently being parsed. Used to resolve
        redirected input files relative to the specification directory.

    pkg_root : Path
        Root path of the package. Used to resolve factory function references
        relative to the package structure.

    Returns
    -------
    Dict[str, UQInputSpec]
        A mapping from input-set name to :class:`UQInputSpec`.

        Each returned input specification contains:
        - ``marginals``: Parsed marginal specification, produced from either a
          list, a template dictionary, or a factory callable.
        - ``copulas``: Always ``None`` in this parser.

    Raises
    ------
    SpecValidationError
        If 'inputs' has an unsupported shape, if a redirected file would
        create a circular reference, or if any input entry is invalid.

    Notes
    -----
    When 'inputs' is a string, it is treated as a filename relative to
    ``spec_file`` and the referenced YAML file is loaded recursively.

    For dictionary-based input specifications, each entry must define a
    ``marginals`` field. The value of ``marginals`` may be one of:

    - a list of explicit marginal definitions
    - a template dictionary defining a shared marginal pattern
    - a factory dictionary containing a ``factory`` reference

    The factory resolution follows the same callable-parsing rules used
    elsewhere in the parser: a plain function name is resolved against the
    YAML file's module context, while dotted references are resolved as
    explicit module paths.
    """

    input_specs: Dict[str, UQInputSpec] = {}

    if isinstance(inputs_value, str) and inputs_value.endswith(".yaml"):
        # --- Redirection to another file
        redirected_file = spec_file.with_name(inputs_value)

        # Must not be identical with the main specification file
        if redirected_file == spec_file:
            raise SpecValidationError(
                f"Input redirection to {inputs_value} would create a circular "
                f"dependency in {str(spec_file)}"
            )

        inputs_ = safe_load(redirected_file)

        return parse_inputs(inputs_, spec_file, pkg_root)

    elif isinstance(inputs_value, dict):
        # --- Parse each of the input specifications
        for key, value in inputs_value.items():
            # Check if required key is present
            validate_required_keys(
                value,
                required_keys={"marginals"},
                context=f"Input {key} of {str(spec_file)}",
            )
            # --- Parse the marginals
            marginals_spec: Union[
                List[MarginalSpec],
                CallableSpec,
                MarginalTemplate,
            ]
            marginals = value["marginals"]

            if isinstance(marginals, list):
                # List of marginals
                marginals_spec = _parse_marginals_list(marginals)

            elif isinstance(marginals, dict):
                if "factory" in marginals:
                    # Factory function
                    marginals_spec = parse_factory(
                        marginals,
                        spec_file,
                        pkg_root,
                    )
                else:
                    marginals_spec = _parse_marginals_template(marginals)
            else:
                raise SpecValidationError(
                    f"Input '{key}' in {spec_file} has unsupported "
                    f"'marginals' value: {marginals!r}"
                )

            input_specs[key] = UQInputSpec(
                name=key,
                marginals=marginals_spec,
                copulas=None,
            )

    else:
        raise SpecValidationError(
            f"Invalid input specification: {inputs_value}"
        )

    return input_specs


# --- Helper functions
def _parse_marginals_template(
    base_marginal: Dict[str, Any],
) -> MarginalTemplate:
    """Parse a template specification for marginal distributions.

    This helper validates and normalizes a single marginal template
    specification. The template defines one shared distribution and parameter
    set for all dimensions, while optional ``name`` and ``description`` fields
    may contain ``$idx`` placeholders that are interpreted later by
    ``MarginalTemplate`` when the the probabilistic input is instantiated.

    Parameters
    ----------
    base_marginal : dict
        Template specification with the following required keys:

        - ``distribution`` (str): Name of the distribution to apply to all
          dimensions.
        - ``parameters`` (list): Distribution parameters. Each entry is
          resolved to a numeric value before constructing the template.

        Optional keys:
        - ``name`` (str): Template for the variable name, may include
          ``$idx``.
        - ``description`` (str): Template for the variable description, may
          include ``$idx``.

    Returns
    -------
    MarginalTemplate
        A normalized marginal template with resolved numeric parameters.

    Raises
    ------
    SpecValidationError
        If the marginal specification is invalid.
    """
    # Validate the marginal dictionary
    validate_marginal(base_marginal)

    # Resolve the distribution parameter values to numeric values
    resolved_parameters = [
        resolve_numeric(p) for p in base_marginal["parameters"]
    ]

    return MarginalTemplate(
        distribution=base_marginal["distribution"],
        parameters=resolved_parameters,
        name=base_marginal.get("name"),
        description=base_marginal.get("description"),
    )


def _parse_marginals_list(marginals: list) -> List[MarginalSpec]:
    """Parse a list of marginal distribution specifications.

    This helper processes a list of marginal specifications, each defining
    a single probabilistic input dimension. Each marginal can optionally
    include a ``repeat`` key to duplicate the specification across multiple
    dimensions with automatic index substitution in name and description.

    Parameters
    ----------
    marginals : list
        List of marginal specification dictionaries. Each dictionary must
        contain:

        - ``distribution`` (str): Name of the distribution.
        - ``parameters`` (list): Distribution parameters.

        Optional keys:
        - ``name`` (str): Variable name, may contain ``$idx`` placeholder.
        - ``description`` (str): Variable description, may contain ``$idx``
          placeholder.
        - ``repeat`` (int): Number of times to repeat this marginal with
          automatic index substitution (starting from 1). The value must be
          a positive integer.

    Returns
    -------
    List[MarginalSpec]
        List of parsed marginal specifications. If a marginal contains a
        ``repeat`` key with value N, it will expand to N consecutive
        MarginalSpec objects with index-substituted names and descriptions.

    Notes
    -----
    When ``repeat`` is specified, the ``$idx`` placeholder in ``name`` and
    ``description`` fields is replaced with sequential indices starting from 1.
    The ``repeat`` keyword is filtered out before validation and construction.
    """

    parsed_marginals: List[MarginalSpec] = []

    for marginal in marginals:

        if "repeat" in marginal:
            # Filter 'repeat' keyword
            base_marginal = {
                k: v for k, v in marginal.items() if k != "repeat"
            }
            # Validate the base marginal
            validate_marginal(base_marginal)
            # Repeat the marginal
            repeat = marginal["repeat"]
            _validate_repeat(repeat)
            for i in range(repeat):
                parsed_marginals.append(
                    _build_marginal_spec(base_marginal, idx=i + 1)
                )
        else:
            # Each marginal is a valid marginal
            validate_marginal(marginal)

            parsed_marginals.append(_build_marginal_spec(marginal))

    return parsed_marginals


def _build_marginal_spec(
    marginal: Dict[str, Any],
    idx: Optional[int] = None,
) -> MarginalSpec:
    """Build a MarginalSpec from a marginal dictionary.

    This helper constructs a single marginal specification from a dictionary,
    resolving numeric parameters and optionally substituting an index value
    into templated name and description fields.

    Parameters
    ----------
    marginal : Dict[str, Any]
        Marginal specification dictionary with required keys:

        - ``distribution`` (str): Name of the distribution.
        - ``parameters`` (list): Distribution parameters to be resolved.

        Optional keys:
        - ``name`` (str): Variable name, may contain ``$idx`` placeholder.
        - ``description`` (str): Variable description, may contain ``$idx``
          placeholder.
    idx : int, optional
        Index value to substitute into ``$idx`` placeholders in the name
        and description fields. If None, no substitution is performed.

    Returns
    -------
    MarginalSpec
        A normalized marginal specification with resolved parameters and
        substituted name/description if an index was provided.
    """
    distribution = marginal["distribution"]
    resolved_parameters = [resolve_numeric(p) for p in marginal["parameters"]]

    name = marginal.get("name")
    description = marginal.get("description")

    if idx is not None:
        name = substitute_idx(name, idx)
        description = substitute_idx(description, idx)

    return MarginalSpec(
        distribution=distribution,
        parameters=resolved_parameters,
        name=name,
        description=description,
    )


def _validate_repeat(repeat: int) -> None:
    """Validate that repeat is a positive integer.

    Parameters
    ----------
    repeat : int
        The repeat count to validate.

    Raises
    ------
    SpecValidationError
        If repeat is not a positive integer.
    """
    if not isinstance(repeat, int) or repeat <= 0:
        raise SpecValidationError(
            f"Invalid repeat value {repeat!r}; expected a positive integer."
        )
