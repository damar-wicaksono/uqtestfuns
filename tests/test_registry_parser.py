import pytest

from pathlib import Path

from uqtestfuns.core.registry.specs import (
    CallableSpec,
    MarginalTemplate,
    UQInputSpec,
    UQParametersSpec,
)
from uqtestfuns.core.registry.parser import parse_spec, SpecValidationError
from uqtestfuns.core.registry.registry_entry import UQTestFunSpec

# Fixture roots
VALID_ROOT = Path(__file__).parent / "fixtures" / "valid_yaml"
INVALID_ROOT = Path(__file__).parent / "fixtures" / "invalid_yaml"

# NOTE: List[MarginalSpec] cannot be checked via isinstance(), use list instead
MARGINALS_SPECS = (list, MarginalTemplate, CallableSpec)

VALID_SPEC_FILES = [
    "sum_of_squares_2d.yaml",
    "sine_sum_6d.yaml",
    "active_inert_10d.yaml",
    "weighted_product.yaml",
    "linear_sum.yaml",
    "circular_bar_2d.yaml",
    "clipped_scaling_3d.yaml",
    "simple_series/variant_sum.yaml",
    "simple_series/variant_prod.yaml",
    "simple_series/variant_max.yaml",
]


@pytest.fixture(params=VALID_SPEC_FILES)
def valid_spec_file(request):
    """Fixture to provide valid YAML specification files for testing."""
    spec_file = VALID_ROOT / request.param

    return spec_file


INVALID_SPEC_FILES = [
    "empty.yaml",
    "invalid_eval.yaml",
    "invalid_eval_no_file.yaml",
    "invalid_expression.yaml",
    "invalid_inputs_literal.yaml",
    "invalid_inputs_recursive.yaml",
    "invalid_marginals_literal.yaml",
    "invalid_marginals_parameters.yaml",
    "invalid_marginals_repeat.yaml",
    "invalid_parameters.yaml",
]


@pytest.fixture(params=INVALID_SPEC_FILES)
def invalid_spec_file(request):
    """Fixture to provide invalid YAML specification files for testing."""
    spec_file = INVALID_ROOT / request.param

    return spec_file


def test_parse_spec_structural(valid_spec_file):
    """Test the specification structure of a valid YAML file."""
    # Parse the specification
    spec = parse_spec(valid_spec_file, VALID_ROOT)

    # Assertions
    assert isinstance(spec, UQTestFunSpec)
    assert spec.name is not None

    # Parsed evaluate
    assert isinstance(spec.evaluate, CallableSpec)

    # Parsed inputs
    assert isinstance(spec.inputs, dict)
    for input_id, input_spec in spec.inputs.items():
        assert isinstance(input_id, str)
        assert isinstance(input_spec, UQInputSpec)
        assert isinstance(input_spec.marginals, MARGINALS_SPECS)

    # Parsed parameters (optional, may be None)
    if spec.parameters is not None:
        assert isinstance(spec.parameters, dict)
        for parameters_id, parameters_spec in spec.parameters.items():
            assert isinstance(parameters_id, str)
            assert isinstance(parameters_spec, UQParametersSpec)
            assert isinstance(parameters_spec.name, str)
            assert isinstance(parameters_spec.values, dict)
            # Keys are always strings
            assert all(
                isinstance(key, str) for key in parameters_spec.values.keys()
            )
            # Descriptions are optional, may be None
            if parameters_spec.keyword_descriptions is not None:
                assert isinstance(parameters_spec.keyword_descriptions, dict)
                for key, value in parameters_spec.keyword_descriptions.items():
                    # Dict[str, str]
                    assert isinstance(key, str)
                    assert isinstance(value, str)


def test_parse_spec_invalid(invalid_spec_file):
    """Test invalid YAML specification files."""
    with pytest.raises(SpecValidationError):
        _ = parse_spec(invalid_spec_file, INVALID_ROOT)
