from uqtestfuns.core.registry.spec_parser import parse_info

from pathlib import Path

FIXTURES_ROOT = Path(__file__).parent / "fixtures" / "valid_yaml"


class TestParseInfo:
    """All tests related to parsing spec files for UQTestFuns."""

    def test_fixed_single_input_no_params(self):
        """Parse spec: fixed-dim, single input, no parameters."""
        yaml_file = FIXTURES_ROOT / "fixed_single_input_no_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert not info.variable_dimension
        assert info.input_dimension == 1
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()

    def test_fixed_multi_inputs_no_params(self):
        """Parse spec: fixed-dim, multiple inputs, no parameters."""
        yaml_file = FIXTURES_ROOT / "fixed_multi_inputs_no_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert not info.variable_dimension
        assert info.input_dimension == 1
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()
        assert len(info.available_input_ids) == 2

    def test_fixed_single_input_fixed_params(self):
        """Parse spec: fixed-dim, single input, fixed parameters."""
        yaml_file = FIXTURES_ROOT / "fixed_single_input_fixed_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert not info.variable_dimension
        assert info.input_dimension == 1
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()
        assert info.available_parameter_ids is not None
        assert len(info.available_parameter_ids) == 2

    def test_var_single_input_no_params(self):
        """Parse spec: variable-dim, single input, no parameters."""
        yaml_file = FIXTURES_ROOT / "var_single_input_no_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert info.variable_dimension
        assert info.input_dimension is None
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()

    def test_var_multi_inputs_no_params(self):
        """Parse spec: variable-dim, multiple inputs, no parameters."""
        yaml_file = FIXTURES_ROOT / "var_multi_inputs_no_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert info.variable_dimension
        assert info.input_dimension is None
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()
        assert len(info.available_input_ids) == 2

    def test_var_single_input_mixed_params(self):
        """Parse spec: variable-dim, single input, mixed parameters."""
        yaml_file = FIXTURES_ROOT / "var_single_input_mixed_params.yaml"
        info = parse_info(yaml_file, FIXTURES_ROOT)

        # Assertions
        assert info.variable_dimension
        assert info.input_dimension is None
        assert info.output_dimension == 1
        assert info.spec_path == yaml_file.resolve()
        assert info.available_parameter_ids is not None
        assert len(info.available_parameter_ids) == 2
