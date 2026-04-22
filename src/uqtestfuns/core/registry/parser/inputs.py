from pathlib import Path
from string import Template
from typing import Any, Dict, List, Optional, Union

from uqtestfuns.core.registry.specs import MarginalSpec, MarginalTemplate, UQInputSpec, CallableSpec

from .utils import safe_load, resolve_numeric, resolve_generic, parse_callable
from .validation import SpecValidationError, validate_marginal


def parse_inputs(
    inputs: Union[str, dict],
    yaml_file: Path,
    pkg_root: Path,
) -> Dict[str, UQInputSpec]:
    """Parse the inputs section of a YAML specification.

    This function parses the 'inputs' field from a YAML specification file
    and constructs a dictionary of UQInputSpec objects that define the
    probabilistic input model for a UQ test function. It supports
    multiple input specification formats, including explicit marginal lists,
    marginal templates, factory functions, and file redirections.

    Parameters
    ----------
    inputs : Union[str, dict]
        The inputs specification from the YAML file. Can be:

        - A string: Path to another YAML file containing the input
          specification (enables input reuse across test functions)
        - A dictionary: Direct specification of input sets, where each key
          is an input set ID and each value contains marginal specifications

    yaml_file : Path
        Path to the YAML specification file being parsed. Used to resolve
        relative paths for file redirections and factory function modules.
    pkg_root : Path
        Root path of the package, used to construct absolute module paths
        for factory functions relative to the package structure.

    Returns
    -------
    Dict[str, UQInputSpec]
        A dictionary mapping input set IDs (strings) to UQInputSpec objects.
        Each UQInputSpec contains:

        - marginals: Specification of marginal distributions (can be a list,
          template, or factory callable)
        - copulas: Specification of dependence structure (currently None,
          reserved for future use)

    Notes
    -----
    The function supports three marginal specification formats:

    1. **List of marginals**: An explicit list where each element defines
       a single marginal distribution with its parameters:

       .. code-block:: yaml

          marginals:
            - distribution: "normal"
              parameters: [0, 1]
              name: "X1"
            - distribution: "uniform"
              parameters: [-1, 1]
              name: "X2"

    2. **Template specification**: A template that defines identical marginals
       for all input dimensions (typically used with variable-dimension
       functions):

       .. code-block:: yaml

          marginals:
            distribution: uniform
            parameters: [0, 1]
            name_template: X_$idx
            describe_template: Variable $idx

    3. **Factory function**: A callable that programmatically generates
       marginals, useful for complex input specifications (by default
       the callable is located in the module with the same name as
       the YAML file):

       .. code-block:: yaml

          marginals:
            factory: create_marginals

    **File Redirection**: When inputs is a string, it's treated as a filename
    relative to the YAML file's directory. The function loads that file and
    recursively parses its 'inputs' section, enabling input specification
    reuse across multiple test functions.

    The factory function specification follows the same resolution rules as
    `parse_evaluate()`: if only a function name is given, the module is
    assumed to have the same name as the YAML file; if a dot-separated path
    is given (e.g., "module.function"), it's resolved relative to the YAML
    file's directory.
    """

    input_specs = {}

    # --- Redirection to another file
    if isinstance(inputs, str) and inputs.endswith(".yaml"):
        inputs_ = safe_load(yaml_file.with_name(inputs))

        return parse_inputs(inputs_, yaml_file, pkg_root)

    # --- Parse the marginals
    for key, value in inputs.items():
        marginals = value["marginals"]

        if isinstance(marginals, list):
            # List of marginals
            marginals_spec = _parse_marginals_list(marginals)

        elif isinstance(marginals, dict):
            if "factory" in marginals.keys():
                # Factory function
                marginals_spec = _parse_marginals_factory(
                    marginals, yaml_file, pkg_root
                )
            else:
                marginals_spec = _parse_marginals_template(marginals)
        else:
            raise SpecValidationError(
                f"Unsupported input specification: {value}"
            )

        input_specs[key] = UQInputSpec(
            marginals=marginals_spec,
            copulas=None,
        )

    return input_specs


def _parse_marginals_list(marginals: List[Dict[str, Any]]) -> List[MarginalSpec]:
    """Parse a list of marginals specifications.
    """
    def _substitute_idx(tpl: Optional[str], idx_: int) -> Optional[str]:
        if tpl is None:
            return None

        return Template(tpl).safe_substitute(idx=idx_)

    parsed_marginals = []
    for marginal in marginals:

        # --- "repeat" as key is possible
        if "repeat" in marginal:
            filtered_marginal = {
                k: v for k, v in marginal.items() if k != "repeat"
            }
            validate_marginal(filtered_marginal)
            repeat_count = marginal["repeat"]
            for idx in range(repeat_count):
                name = _substitute_idx(
                    filtered_marginal.get("name", None),
                    idx+1,
                )
                description = _substitute_idx(
                    filtered_marginal.get("description", None),
                    idx+1,
                )
                parameters = filtered_marginal["parameters"]
                parameters = [
                    resolve_numeric(parameter) for parameter in parameters
                ]
                parsed_marginals.append(
                    MarginalSpec(
                        filtered_marginal["distribution"],
                        parameters,
                        name,
                        description,
                    )
                )
        else:

            # --- Validate marginal dictionary
            validate_marginal(marginal)

            # --- Convert to marginal spec
            distribution = marginal["distribution"]
            parameters = marginal["parameters"]
            parameters = [
                resolve_numeric(parameter) for parameter in parameters
            ]
            name = marginal.get("name", None)
            description = marginal.get("description", None)

            parsed_marginals.append(
                MarginalSpec(distribution, parameters, name, description)
            )

    return parsed_marginals


def _parse_marginals_factory(
    marginals: Dict[str, Any],
    yaml_file: Path,
    pkg_root: Path,
) -> CallableSpec:
    """Parse a factory function specification for marginal distributions."""

    module_path, callable_name = parse_callable(marginals["factory"], yaml_file, pkg_root)

    # Parse kwargs
    kwargs = {k: resolve_generic(v) for k, v in marginals.items() if k != "factory"}
    if not kwargs:
        kwargs = None

    return CallableSpec(
        module_path=module_path,
        function_name=callable_name,
        kwargs=kwargs,
    )


def _parse_marginals_template(marginals: Dict[str, Any]) -> MarginalTemplate:
    """Parse a template specification for marginal distributions.

    This helper function processes a template-based marginal specification
    where all marginal distributions share the same distribution type and
    parameters. This format is particularly useful for variable-dimension
    test functions where the input dimension can vary, but all marginals
    follow the same pattern. The template supports optional name and
    description templates that can include placeholders for dimension indices.

    Parameters
    ----------
    marginals : dict
        A dictionary defining the marginal distribution template with the
        following keys:

        - distribution (str, required): Name of the probability distribution
          to be applied to all marginals (e.g., "normal", "uniform")
        - parameters (list, required): Distribution parameters as a list
          (e.g., [0, 1] for standard normal, [-1, 1] for uniform bounds)
        - name_template (str, optional): Template string for generating
          marginal names, can include $idx placeholder for dimension index
          (e.g., "X$idx" generates "X1", "X2", etc.)
        - description_template (str, optional): Template string for generating
          marginal descriptions, can include $idx placeholder for dimension
          index (e.g., "Variable $idx")

    Returns
    -------
    MarginalTemplate
        A MarginalTemplate object containing the distribution type, parameters,
        and optional name and description templates. This template can be
        instantiated for any number of dimensions at runtime.

    Raises
    ------
    SpecValidationError
        If the required "distribution" or "parameters" field is missing from
        the marginals' dictionary.
    """
    # Obligatory field must exist per entry
    validate_marginal(marginals)

    parameters_ = [resolve_numeric(p) for p in marginals["parameters"]]
    return MarginalTemplate(
        distribution=marginals["distribution"],
        parameters=parameters_,
        name=marginals.get("name", None),
        description=marginals.get("description", None),
    )