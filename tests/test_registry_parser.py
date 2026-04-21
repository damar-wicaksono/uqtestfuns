import pytest
import yaml

from pathlib import Path

from uqtestfuns.core.registry.parser import parse_evaluate
from uqtestfuns.core.registry.specs import CallableSpec
from uqtestfuns.core.registry.validation import SpecValidationError

FIXTURES_ROOT = Path(__file__).parent / "fixtures" / "valid_yaml"


class TestParseEvaluate:
    """All tests related to parsing the evaluate section of YAML files."""

    def test_empty_evaluate(self):
        """Test parsing an empty evaluate section."""
        yaml_file = FIXTURES_ROOT / "otlcircuit.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the evaluate section
        evaluate_ = data.get("evaluate", None)
        evaluate = parse_evaluate(evaluate_, yaml_file, FIXTURES_ROOT)

        # Assertions
        assert evaluate_ is None
        assert isinstance(evaluate, CallableSpec)
        assert evaluate.function_name == "evaluate"
        assert evaluate.module_path == "valid_yaml.otlcircuit"
        assert evaluate.kwargs is None

    def test_callable_name(self):
        """Test parsing a callable name."""
        yaml_file = FIXTURES_ROOT / "saltelli_linear.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the evaluate section
        evaluate_ = data.get("evaluate", None)
        evaluate = parse_evaluate(evaluate_, yaml_file, FIXTURES_ROOT)

        # Assertions
        assert isinstance(evaluate, CallableSpec)
        assert evaluate.function_name == "compute"
        assert evaluate.module_path == "valid_yaml.saltelli_linear"
        assert evaluate.kwargs is None

    def test_fully_qualified(self):
        """Test parsing a fully qualified function name."""
        yaml_file = FIXTURES_ROOT / "dette8d.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the evaluate section
        evaluate_ = data.get("evaluate", None)
        evaluate = parse_evaluate(evaluate_, yaml_file, FIXTURES_ROOT)

        # Assertions
        assert isinstance(evaluate, CallableSpec)
        assert evaluate.function_name == "evaluate_8d"
        assert evaluate.module_path == "valid_yaml.dette"
        assert evaluate.kwargs is None

    def test_no_module_file(self):
        """Test parsing a YAML without the corresponding module file."""
        root = Path(__file__).parent / "fixtures" / "invalid_yaml"
        yaml_file = root / "invalid_eval_no_file.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the evaluate section
        evaluate_ = data.get("evaluate", None)

        # Assertion
        with pytest.raises(SpecValidationError):
            _ = parse_evaluate(evaluate_, yaml_file, FIXTURES_ROOT)
