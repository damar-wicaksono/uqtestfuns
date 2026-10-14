"""Parser for the output shape function of the YAML specification files.

This module parses the ``output`` field of the ``dimensions`` block when it
names a shape function, constructing a ``CallableSpec`` that is resolved during
instance construction and invoked whenever the instance's output shape is read.
"""

from pathlib import Path

from uqtestfuns.core.registry.specs import CallableSpec

from .utils import parse_callable


def parse_output_shape(
    output_shape: str,
    spec_file: Path,
    pkg_root: Path,
) -> CallableSpec:
    """Parse an output shape function name into a CallableSpec.

    Called when ``dimensions.output`` in the YAML is a string, meaning the
    output shape is not fixed but computed by a function at instantiation time.
    Resolves the module path and function name using the same conventions as
    the evaluate parser: a bare name defaults to the same-stem module, while
    a dotted name (``module.function``) is resolved explicitly.

    Parameters
    ----------
    output_shape : str
        The value of ``dimensions.output`` from the YAML file: either a
        function name (resolved from the same-stem module) or a fully
        qualified ``module.function`` string.
    spec_file : Path
        Path to the YAML specification file, used to resolve the default
        module when only a function name is given.
    pkg_root : Path
        Root path of the package, used to construct the absolute module path.

    Returns
    -------
    CallableSpec
        Specification object identifying the shape function; resolved to a
        callable by the resolver at instantiation time.
    """
    module_path, evaluate_name = parse_callable(
        output_shape,
        spec_file,
        pkg_root,
    )

    return CallableSpec(
        module_path=module_path,
        function_name=evaluate_name,
        kwargs=None,
    )
