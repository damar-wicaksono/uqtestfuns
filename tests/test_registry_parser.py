import pytest
import yaml

from pathlib import Path

from uqtestfuns.core.registry.parser.evaluate import parse_evaluate
from uqtestfuns.core.registry.parser.inputs import parse_inputs
from uqtestfuns.core.registry.parser.parameters import parse_parameters
from uqtestfuns.core.registry.specs import CallableSpec, UQInputSpec, UQParametersSpec
from uqtestfuns.core.registry.parser.validation import SpecValidationError

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

    def test_fully_qualified_family(self):
        """Test parsing a fully qualified function name."""
        yaml_file = FIXTURES_ROOT / "franke" / "franke_1.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the evaluate section
        evaluate_ = data.get("evaluate", None)
        evaluate = parse_evaluate(evaluate_, yaml_file, FIXTURES_ROOT)

        # Assertions
        assert isinstance(evaluate, CallableSpec)
        assert evaluate.function_name == "franke_1"
        assert evaluate.module_path == "valid_yaml.franke.evaluate"
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
            _ = parse_evaluate(evaluate_, yaml_file, root)


class TestParseMarginalsList:
    """All tests related to parsing the marginals list."""

    def test_standard(self):
        yaml_file = FIXTURES_ROOT / "otlcircuit.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        inputs = parse_inputs(data["inputs"], yaml_file, FIXTURES_ROOT)

        # Assertion
        for input_id, input_spec in inputs.items():
            assert isinstance(input_spec, UQInputSpec)
            if isinstance(input_spec.marginals, list):
                assert len(input_spec.marginals) == data["dimensions"]["input"]

    def test_repeat(self):
        yaml_file = FIXTURES_ROOT / "otlcircuit20d.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        inputs = parse_inputs(data["inputs"], yaml_file, FIXTURES_ROOT)
        for input_id, input_spec in inputs.items():
            assert isinstance(input_spec, UQInputSpec)
            if isinstance(input_spec.marginals, list):
                assert len(input_spec.marginals) == data["dimensions"]["input"]

    def test_factory(self):
        yaml_file = FIXTURES_ROOT / "saltelli_linear.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        inputs = parse_inputs(data["inputs"], yaml_file, FIXTURES_ROOT)
        for input_id, input_spec in inputs.items():
            assert isinstance(input_spec, UQInputSpec)

    def test_template(self):
        yaml_file = FIXTURES_ROOT / "sobol_g.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        inputs = parse_inputs(data["inputs"], yaml_file, FIXTURES_ROOT)
        for input_id, input_spec in inputs.items():
            assert isinstance(input_spec, UQInputSpec)

    def test_redirect(self):
        yaml_file = FIXTURES_ROOT / "franke" / "franke_1.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        inputs = parse_inputs(data["inputs"], yaml_file, FIXTURES_ROOT)
        for input_id, input_spec in inputs.items():
            assert isinstance(input_spec, UQInputSpec)

    def test_invalid(self):
        root = Path(__file__).parent / "fixtures" / "invalid_yaml"
        yaml_file = root / "invalid_inputs.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the input section
        with pytest.raises(SpecValidationError):
            _ = parse_inputs(data["inputs"], yaml_file, root)


class TestParseParameters:
    """All tests related to parsing the parameters section."""

    def test_simple(self):
        yaml_file = FIXTURES_ROOT / "ishigami.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the parameters section
        parameters = parse_parameters(data["parameters"], yaml_file, FIXTURES_ROOT)

        # Assertions
        for parameter_id, parameter_spec in parameters.items():
            assert isinstance(parameter_spec, UQParametersSpec)

    def test_callable(self):
        yaml_file = FIXTURES_ROOT / "sobol_g.yaml"
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Parse the parameters section
        parameters = parse_parameters(data["parameters"], yaml_file, FIXTURES_ROOT)

        # Assertions
        for parameter_id, parameter_spec in parameters.items():
            assert isinstance(parameter_spec, UQParametersSpec)
