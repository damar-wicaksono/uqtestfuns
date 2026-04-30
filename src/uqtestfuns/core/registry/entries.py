"""Registry entry data structures for UQ test function metadata.

This module defines the data structures used to store metadata about
uncertainty quantification (UQ) test functions in the registry.
The metadata is parsed from YAML specification files and used for
function discovery and instantiation.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from pathlib import Path
from typing_extensions import TypedDict

from .specs import CallableSpec, UQInputSpec, UQParametersSpec


class KeywordInfo(TypedDict):
    """Type definition for parameter keyword metadata.

    Attributes
    ----------
    type : Any
        The Python type of the parameter keyword value.
    description : Optional[str]
        Human-readable description of the parameter keyword.
    """

    type: Any
    description: Optional[str]


@dataclass(frozen=True)
class UQTestFunInfo:
    """Registry entry containing metadata about a UQ test function.

    This class stores enough information about a test function parsed
    from its YAML specification file required for its discovery. This includes
    its name, description, dimensionality properties,
    and available input/parameter configurations.

    Parameters
    ----------
    name : str
        Unique identifier for the test function.
    description : str
        Human-readable description of the test function.
    tags : List[str]
        List of categorical tags for classification and search.
    variable_dimension : bool
        Whether the function supports variable input dimensions.
    input_dimension : Optional[int]
        Number of input dimensions (None if variable_dimension is True).
    output_dimension : int
        Number of output dimensions (default is 1).
    spec_path : Path
        Absolute path to the YAML specification file
        for the next targeted read.
    available_input_ids : Dict[str, str]
        Mapping of input IDs to their descriptions.
    default_input_id : str
        Identifier for the default input configuration.
    available_parameter_ids : Optional[Dict[str, str]], optional
        Mapping of parameter IDs to their descriptions (default is None).
    default_parameter_id : Optional[str], optional
        Identifier for the default parameter configuration (default is None).
    parameter_keywords : Optional[Dict[str, KeywordInfo]], optional
        Mapping of parameter keywords to their type and description
        (default is None).
    """

    # Identity
    name: str
    description: str
    tags: List[str]

    # Dimension info
    variable_dimension: bool
    input_dimension: Optional[int]
    output_dimension: int

    # File references
    spec_path: Path

    # Input variant IDs
    available_input_ids: Dict[str, str]
    default_input_id: str

    # Parameter variant IDs
    available_parameter_ids: Optional[Dict[str, str]] = None
    default_parameter_id: Optional[str] = None
    parameter_keywords: Optional[Dict[str, KeywordInfo]] = None


@dataclass(frozen=True)
class UQTestFunSpec:
    """Complete specification for a UQ test function.

    This class represents the full specification of a UQ test function
    parsed from a YAML specification file. It contains all the detailed
    information needed to instantiate and execute the test function,
    including the evaluation callable, input configurations, and optional
    parameter configurations.

    Parameters
    ----------
    name : str
        Unique identifier for the test function.
    evaluate : CallableSpec
        Specification of the callable that evaluates the test function,
        including module path and function name.
    inputs : Dict[str, UQInputSpec]
        Mapping of input IDs to their complete specifications, including
        marginal distributions and other input-related metadata.
    parameters : Optional[Dict[str, UQParametersSpec]], optional
        Mapping of parameter IDs to their complete specifications
        (default is None). Used for test functions that support
        multiple parameter configurations.
    """

    name: str
    evaluate: CallableSpec
    inputs: Dict[str, UQInputSpec]
    parameters: Optional[Dict[str, UQParametersSpec]]
